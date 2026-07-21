"""Released-scale (d=20, tau=5, 200-run) clean-room linear-regression protocol.

The source specifies dimensions, sketches, tau, 200 independent runs, and
phi_t=(t+1)^-.501, but does not disclose its horizon or executable code.  This
script therefore records its horizon explicitly and never claims Table parity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from nasketch import parameters, projection, solve_lyapunov


def kaczmarz_parameters(B: np.ndarray) -> tuple[float, float, float]:
    d = len(B)
    projections = [projection(B, np.eye(d)[:, [i]]) for i in range(d)]
    Z = sum(projections) / d
    mu = float(np.linalg.eigvalsh(Z)[0])
    E = sum(P @ np.linalg.solve(Z, P) for P in projections) / d
    chol = np.linalg.cholesky(Z)
    inv_chol = np.linalg.inv(chol)
    nu = float(np.linalg.eigvalsh(inv_chol @ E @ inv_chol.T)[-1])
    return (*parameters(mu, nu), mu, nu)


def sampled_operator(B: np.ndarray, alpha: float, beta: float, gamma: float,
                     tau: int, samples: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Independent Monte Carlo oracle for K and Gamma in Theorem 4.3."""
    d = len(B)
    indices = rng.integers(d, size=(samples, tau))
    columns = B.T.copy()  # rows are B e_i (B is symmetric)
    denom = np.sum(columns * columns, axis=1)
    delta = np.broadcast_to(np.eye(d), (samples, d, d))
    z = np.zeros_like(delta)
    v = np.zeros_like(delta)
    for j in range(tau):
        y = alpha*v + (1-alpha)*z
        residual = np.einsum("nij,jk->nik", y-delta, B)
        ids = indices[:, j]
        scalar = residual[np.arange(samples), ids, :]
        omega = columns[ids, :, None] * scalar[:, None, :] / denom[ids, None, None]
        z = y - omega
        v = beta*v + (1-beta)*y - gamma*omega
    # With Delta=I, Algorithm 1 gives z=(I-Ktilde) Delta.
    K = np.eye(d) - z.mean(axis=0)
    gamma_star = np.einsum("nij,nkj->ik", z, z) / samples  # Omega=I in this model
    return K, gamma_star


def run(B: np.ndarray, x_star: np.ndarray, alpha: float, beta: float, gamma: float,
        tau: int, reps: int, horizon: int, checkpoints: set[int], rng: np.random.Generator):
    """Vectorized 200-independent-run outer update using literal Algorithm 1."""
    d = len(B)
    chol = np.linalg.cholesky(B)
    x = np.zeros((reps, d))
    z = np.zeros((reps, d))
    v = np.zeros((reps, d))
    columns = B.T.copy()
    denom = np.sum(columns * columns, axis=1)
    sum_x = np.zeros_like(x)
    sum_wxx = np.zeros((reps, d, d))
    sum_w = 0.0
    snapshots = {}
    for t in range(horizon):
        phi = (t + 1.0) ** -.501
        a = rng.normal(size=(reps, d)) @ chol.T
        noise = rng.normal(size=reps)
        residual = np.sum(a * (x-x_star), axis=1) - noise
        g = a * residual[:, None]
        z.fill(0.0)
        v.fill(0.0)
        for _ in range(tau):
            y = alpha*v + (1-alpha)*z
            rhs = y @ B.T + g
            ids = rng.integers(d, size=reps)
            scalar = rhs[np.arange(reps), ids]
            omega = columns[ids] * scalar[:, None] / denom[ids, None]
            z = y - omega
            v = beta*v + (1-beta)*y - gamma*omega
        x += phi*z
        sum_x += x
        sum_wxx += np.einsum("ni,nj,n->nij", x, x, np.full(reps, 1.0/phi))
        sum_w += 1.0/phi
        when = t + 1
        if when in checkpoints:
            mean = sum_x / when
            weighted = sum_wxx / when - (sum_w/when) * np.einsum("ni,nj->nij", mean, mean)
            snapshots[when] = {"x": x.copy(), "covariance_estimate": weighted.mean(axis=0)}
    return snapshots


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--horizon", type=int, default=8000)
    parser.add_argument("--reps", type=int, default=200)
    parser.add_argument("--operator-samples", type=int, default=20000)
    args = parser.parse_args()
    d, tau = 20, 5
    r = .4
    B = r ** np.abs(np.subtract.outer(np.arange(d), np.arange(d)))
    x_star = np.linspace(0.0, 1.0, d)
    alpha, beta, gamma, mu, nu = kaczmarz_parameters(B)
    K, gamma_star = sampled_operator(B, alpha, beta, gamma, tau, args.operator_samples,
                                     np.random.default_rng(1))
    target = solve_lyapunov(np.eye(d)-K, gamma_star)
    checkpoints = {args.horizon // 4, args.horizon // 2, args.horizon}
    snapshots = run(B, x_star, alpha, beta, gamma, tau, args.reps, args.horizon, checkpoints,
                    np.random.default_rng(2))
    report = {"protocol": {"d": d, "covariance": "Toeplitz r=.4", "tau": tau,
                            "sketch": "Kaczmarz", "runs": args.reps, "horizon": args.horizon,
                            "stepsize": "(t+1)^-.501"},
              "parameters": {"alpha": alpha, "beta": beta, "gamma": gamma, "mu": mu, "nu": nu},
              "operator_samples": args.operator_samples, "checkpoints": {}}
    errors = []
    for t, value in sorted(snapshots.items()):
        scaled = value["x"] / np.sqrt((t + 1.0) ** -.501)
        empirical = np.cov(scaled, rowvar=False, bias=True)
        clt_error = float(np.linalg.norm(empirical-target, "fro") / np.linalg.norm(target, "fro"))
        estimator_error = float(np.linalg.norm(value["covariance_estimate"]-target, "fro") / np.linalg.norm(target, "fro"))
        errors.append(estimator_error)
        report["checkpoints"][str(t)] = {"scaled_covariance_relative_error": clt_error,
                                           "online_estimator_relative_error": estimator_error,
                                           "mean_distance": float(np.mean(np.linalg.norm(value["x"]-x_star, axis=1)))}
    report["covariance_estimator_log_slope"] = float(np.polyfit(np.log(sorted(snapshots)), np.log(errors), 1)[0])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
