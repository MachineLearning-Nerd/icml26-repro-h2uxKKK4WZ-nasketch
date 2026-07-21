# Claims 2-4


---
<!-- trackio-cell
{"type": "code", "id": "cell_76e7cb94c2b5", "created_at": "2026-07-21T03:47:29+00:00", "title": "Independent theorem-instance audit", "command": ["python", "repro/src/theorem_audits.py", "--out", "outputs/theorem_audits.json"], "exit_code": 0, "duration_s": 3.082}
-->
````bash
$ python repro/src/theorem_audits.py --out outputs/theorem_audits.json
````

exit 0 · 3.1s


````python title=theorem_audits.py
"""Independent theorem-instance audits for arXiv:2604.23436.

These are clean-room checks of the exact recurrences and sufficient conditions
in Theorems 3.8, 4.3 and 4.6. They are deliberately separate from the failed
attempt to recreate the unreleased experimental parameter-approximation code.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from nasketch import solve_lyapunov


def normality_audit(rng: np.random.Generator) -> dict:
    """Theorem 4.3 with a nonzero sketch operator and non-Gaussian noise."""
    d, runs, horizon = 6, 2400, 4000
    K = np.diag(np.linspace(.05, .30, d))
    A = np.eye(d) - K
    raw = rng.normal(size=(d, d))
    Gamma = raw @ raw.T / d + .25*np.eye(d)
    factor = np.linalg.cholesky(Gamma)
    drift = A - .5*np.eye(d)  # zeta=1/(2C_phi), C_phi=1 and phi=1
    target = solve_lyapunov(drift, Gamma)
    x = np.zeros((runs, d))
    for t in range(1, horizon+1):
        # Centered exponential innovations ensure Gaussianity is a limit result.
        innovation = (rng.exponential(size=(runs, d))-1.0) @ factor.T
        x -= (x @ A.T + innovation) / (t+1.0)
    scaled = x * np.sqrt(horizon+1.0)
    empirical = np.cov(scaled, rowvar=False, bias=True)
    order = np.sort(scaled / np.sqrt(np.diag(target)), axis=0)
    gaussian = np.sort(rng.normal(size=(100000, d)), axis=0)[
        np.linspace(0, 99999, runs, dtype=int)]
    qq_r2 = [float(np.corrcoef(order[:, j], gaussian[:, j])[0, 1]**2) for j in range(d)]
    standardized = (scaled-scaled.mean(0))/scaled.std(0)
    return {
        "dimension": d, "independent_last_iterates": runs, "horizon": horizon,
        "stepsize": "1/(t+1)", "innovation": "centered exponential", "K_diagonal": np.diag(K).tolist(),
        "relative_covariance_error": float(np.linalg.norm(empirical-target, "fro")/np.linalg.norm(target, "fro")),
        "lyapunov_residual": float(np.max(np.abs(drift@target + target@drift.T-Gamma))),
        "minimum_qq_r2": min(qq_r2),
        "maximum_abs_skew": float(np.max(np.abs(np.mean(standardized**3, axis=0)))),
        "maximum_abs_excess_kurtosis": float(np.max(np.abs(np.mean(standardized**4, axis=0)-3))),
    }


def covariance_audit(rng: np.random.Generator) -> dict:
    """Theorem 4.6: the literal weighted online estimator, no stored paths."""
    d, runs, horizon, power = 3, 500, 24000, .75
    Omega = np.array([[1., .3, -.2], [.3, .8, .25], [-.2, .25, .7]])
    factor = np.linalg.cholesky(Omega)
    target = Omega/2.0
    checkpoints = (1500, 3000, 6000, 12000, 24000)
    x = np.zeros((runs, d)); sum_x = np.zeros_like(x); sum_wx = np.zeros_like(x)
    sum_wxx = np.zeros((runs, d, d)); sum_w = 0.0; rows = []
    for t in range(1, horizon+1):
        phi = .8/t**power
        eps = (rng.exponential(size=(runs, d))-1.0) @ factor.T
        x -= phi*(x+eps)
        weight = 1.0/phi
        sum_x += x; sum_wx += weight*x
        sum_wxx += weight*np.einsum("ni,nj->nij", x, x); sum_w += weight
        if t in checkpoints:
            mean = sum_x/t
            estimate = (sum_wxx - np.einsum("ni,nj->nij",sum_wx,mean)
                        -np.einsum("ni,nj->nij",mean,sum_wx)
                        +sum_w*np.einsum("ni,nj->nij",mean,mean))/t
            errors = np.linalg.norm(estimate-target, axis=(1,2))
            rows.append({"horizon": t, "mean_frobenius_error": float(errors.mean()),
                         "mean_estimate_relative_error": float(np.linalg.norm(estimate.mean(0)-target,"fro")/np.linalg.norm(target,"fro")),
                         "theory_rate_proxy": float(1/np.sqrt(t*phi))})
    slope = float(np.polyfit(np.log([r["horizon"] for r in rows]), np.log([r["mean_frobenius_error"] for r in rows]), 1)[0])
    return {"dimension": d, "independent_streams": runs, "maximum_horizon": horizon,
            "stepsize": ".8/t^.75", "checkpoints": rows,
            "fitted_error_slope": slope, "theory_rate_slope": -(1-power)/2,
            "online_state": "sum(x), sum(x/phi), sum(xx^T/phi), sum(1/phi)"}


def global_convergence_audit(rng: np.random.Generator) -> dict:
    """Theorem 3.8 on a globally strongly-convex nonlinear objective."""
    d, tau, horizon = 4, 24, 4000
    base, nonlinear = np.array([1.,1.5,2.2,3.]), .2
    gamma_h, upsilon_h = 1., 3.2
    mu, nu = 1/d, float(d)  # uniform-coordinate Kaczmarz
    rate = 1-np.sqrt(mu/nu)
    condition_lhs, condition_rhs = tau*rate**(tau-2), gamma_h/(4*upsilon_h)
    rows=[]
    for radius in (1.,10.,100.):
        x = rng.normal(size=(12,d)); x *= radius/np.linalg.norm(x,axis=1,keepdims=True)
        B = base + nonlinear/np.cosh(np.clip(x,-40,40))**2
        starts=np.linalg.norm(x,axis=1); checkpoints={0: starts.copy()}
        for t in range(horizon):
            hessian=base+nonlinear/np.cosh(np.clip(x,-40,40))**2
            B=(t*B+hessian)/(t+1)
            gradient=base*x+nonlinear*np.tanh(x)+.02*rng.choice((-1.,1.),size=x.shape)
            selected=np.zeros((12,d),dtype=bool)
            choices=rng.integers(d,size=(12,tau))
            selected[np.arange(12)[:,None],choices]=True
            direction=np.where(selected,-gradient/B,0.)  # exact gamma=1 coordinate solver
            x += .8/(t+1)**.75*direction
            if t+1 in (10,50,200,1000,4000): checkpoints[t+1]=np.linalg.norm(x,axis=1)
        rows.append({"initial_radius":radius, "mean_distance_by_checkpoint": [float(checkpoints[k].mean()) for k in (0,10,50,200,1000,4000)],
                     "maximum_final_over_initial":float(np.max(checkpoints[4000]/starts))})
    return {"objective":".5 sum base_i*x_i^2 + .2 sum log(cosh(x_i))", "dimension":d,
            "sketch":"uniform coordinate", "mu":mu,"nu":nu,"gamma":1.,"tau":tau,
            "tau_condition_lhs":condition_lhs,"tau_condition_rhs":condition_rhs,
            "tau_condition_satisfied":bool(condition_lhs<=condition_rhs),"trajectories":36,"horizon":horizon,"rows":rows}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--out",type=Path,required=True); args=parser.parse_args()
    rng=np.random.default_rng(260423436)
    result={"normality":normality_audit(rng),"online_covariance":covariance_audit(rng),"global_convergence":global_convergence_audit(rng)}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()

````


````json title=theorem_audits.json
{
  "normality": {
    "dimension": 6,
    "independent_last_iterates": 2400,
    "horizon": 4000,
    "stepsize": "1/(t+1)",
    "innovation": "centered exponential",
    "K_diagonal": [
      0.05,
      0.1,
      0.15000000000000002,
      0.2,
      0.25,
      0.3
    ],
    "relative_covariance_error": 0.07312073623430071,
    "lyapunov_residual": 5.551115123125783e-17,
    "minimum_qq_r2": 0.997658284850011,
    "maximum_abs_skew": 0.08847347303482335,
    "maximum_abs_excess_kurtosis": 0.16960531774584942
  },
  "online_covariance": {
    "dimension": 3,
    "independent_streams": 500,
    "maximum_horizon": 24000,
    "stepsize": ".8/t^.75",
    "checkpoints": [
      {
        "horizon": 1500,
        "mean_frobenius_error": 0.3925508618102948,
        "mean_estimate_relative_error": 0.09811173739484638,
        "theory_rate_proxy": 0.44817084324637063
      },
      {
        "horizon": 3000,
        "mean_frobenius_error": 0.36531335331127524,
        "mean_estimate_relative_error": 0.10010840700882244,
        "theory_rate_proxy": 0.41097447530336884
      },
      {
        "horizon": 6000,
        "mean_frobenius_error": 0.341923978505284,
        "mean_estimate_relative_error": 0.09669492876405124,
        "theory_rate_proxy": 0.3768652555071075
      },
      {
        "horizon": 12000,
        "mean_frobenius_error": 0.3193088916007353,
        "mean_estimate_relative_error": 0.06051415683570453,
        "theory_rate_proxy": 0.34558696304337905
      },
      {
        "horizon": 24000,
        "mean_frobenius_error": 0.3067180353199054,
        "mean_estimate_relative_error": 0.0353443555029353,
        "theory_rate_proxy": 0.31690464238960186
      }
    ],
    "fitted_error_slope": -0.0906114945109318,
    "theory_rate_slope": -0.125,
    "online_state": "sum(x), sum(x/phi), sum(xx^T/phi), sum(1/phi)"
  },
  "global_convergence": {
    "objective": ".5 sum base_i*x_i^2 + .2 sum log(cosh(x_i))",
    "dimension": 4,
    "sketch": "uniform coordinate",
    "mu": 0.25,
    "nu": 4.0,
    "gamma": 1.0,
    "tau": 24,
    "tau_condition_lhs": 0.04281136117560891,
    "tau_condition_rhs": 0.078125,
    "tau_condition_satisfied": true,
    "trajectories": 36,
    "horizon": 4000,
    "rows": [
      {
        "initial_radius": 1.0,
        "mean_distance_by_checkpoint": [
          1.0,
          0.014949309495041955,
          0.004480946828548337,
          0.0021086694944178227,
          0.001055168798273788,
          0.0006275461146500293
        ],
        "maximum_final_over_initial": 0.0010536085542680038
      },
      {
        "initial_radius": 10.0,
        "mean_distance_by_checkpoint": [
          10.0,
          0.11479370579194108,
          0.006602335689179869,
          0.0019814644517625207,
          0.0008661156718883775,
          0.0006284157754336111
        ],
        "maximum_final_over_initial": 0.00013772788108703062
      },
      {
        "initial_radius": 100.0,
        "mean_distance_by_checkpoint": [
          100.0,
          1.2952437118098274,
          0.06401293017424985,
          0.002382770574161416,
          0.0010547448349919424,
          0.0007170561741565986
        ],
        "maximum_final_over_initial": 1.5133025170115735e-05
      }
    ]
  }
}

````


````output
{
  "normality": {
    "dimension": 6,
    "independent_last_iterates": 2400,
    "horizon": 4000,
    "stepsize": "1/(t+1)",
    "innovation": "centered exponential",
    "K_diagonal": [
      0.05,
      0.1,
      0.15000000000000002,
      0.2,
      0.25,
      0.3
    ],
    "relative_covariance_error": 0.07312073623430071,
    "lyapunov_residual": 5.551115123125783e-17,
    "minimum_qq_r2": 0.997658284850011,
    "maximum_abs_skew": 0.08847347303482335,
    "maximum_abs_excess_kurtosis": 0.16960531774584942
  },
  "online_covariance": {
    "dimension": 3,
    "independent_streams": 500,
    "maximum_horizon": 24000,
    "stepsize": ".8/t^.75",
    "checkpoints": [
      {
        "horizon": 1500,
        "mean_frobenius_error": 0.3925508618102948,
        "mean_estimate_relative_error": 0.09811173739484638,
        "theory_rate_proxy": 0.44817084324637063
      },
      {
        "horizon": 3000,
        "mean_frobenius_error": 0.36531335331127524,
        "mean_estimate_relative_error": 0.10010840700882244,
        "theory_rate_proxy": 0.41097447530336884
      },
      {
        "horizon": 6000,
        "mean_frobenius_error": 0.341923978505284,
        "mean_estimate_relative_error": 0.09669492876405124,
        "theory_rate_proxy": 0.3768652555071075
      },
      {
        "horizon": 12000,
        "mean_frobenius_error": 0.3193088916007353,
        "mean_estimate_relative_error": 0.06051415683570453,
        "theory_rate_proxy": 0.34558696304337905
      },
      {
        "horizon": 24000,
        "mean_frobenius_error": 0.3067180353199054,
        "mean_estimate_relative_error": 0.0353443555029353,
        "theory_rate_proxy": 0.31690464238960186
      }
    ],
    "fitted_error_slope": -0.0906114945109318,
    "theory_rate_slope": -0.125,
    "online_state": "sum(x), sum(x/phi), sum(xx^T/phi), sum(1/phi)"
  },
  "global_convergence": {
    "objective": ".5 sum base_i*x_i^2 + .2 sum log(cosh(x_i))",
    "dimension": 4,
    "sketch": "uniform coordinate",
    "mu": 0.25,
    "nu": 4.0,
    "gamma": 1.0,
    "tau": 24,
    "tau_condition_lhs": 0.04281136117560891,
    "tau_condition_rhs": 0.078125,
    "tau_condition_satisfied": true,
    "trajectories": 36,
    "horizon": 4000,
    "rows": [
      {
        "initial_radius": 1.0,
        "mean_distance_by_checkpoint": [
          1.0,
          0.014949309495041955,
          0.004480946828548337,
          0.0021086694944178227,
          0.001055168798273788,
          0.0006275461146500293
        ],
        "maximum_final_over_initial": 0.0010536085542680038
      },
      {
        "initial_radius": 10.0,
        "mean_distance_by_checkpoint": [
          10.0,
          0.11479370579194108,
          0.006602335689179869,
          0.0019814644517625207,
          0.0008661156718883775,
          0.0006284157754336111
        ],
        "maximum_final_over_initial": 0.00013772788108703062
      },
      {
        "initial_radius": 100.0,
        "mean_distance_by_checkpoint": [
          100.0,
          1.2952437118098274,
          0.06401293017424985,
          0.002382770574161416,
          0.0010547448349919424,
          0.0007170561741565986
        ],
        "maximum_final_over_initial": 1.5133025170115735e-05
      }
    ]
  }
}

````
