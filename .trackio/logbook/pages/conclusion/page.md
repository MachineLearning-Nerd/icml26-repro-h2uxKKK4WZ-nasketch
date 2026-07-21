# Conclusion

## Executive summary

All six anchored claims pass the local, fail-closed clean-room gate. The independent evidence includes 220,011 spectral cells, 2,400 non-Gaussian last-iterate samples, 500 online covariance streams to horizon 24,000, and 36 global-convergence trajectories from three distant radii. The source's unreleased empirical `mu`/`nu` approximation prevents a literal Table/Figure replication; the resulting `tau=5` pilot diverges and is preserved as negative evidence rather than hidden or substituted.

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | Six theorem-instance audits of Algorithm 1 and stated results | Exact unpublished regression experiment code, parameter approximations, figures, and tables |
| Hardware | Local CPU / 15 GB RAM | Undisclosed by the authors |
| Time | Deterministic audits plus 2,400+500 stochastic streams | Unknown; cannot be measured without released procedure |
| Cost | Local CPU | Unknown |
| Outcome | Six local claim checks pass; source experiment mismatch disclosed | Not established because key source procedure is unavailable |


---
<!-- trackio-cell
{"type": "code", "id": "cell_c7039fc82159", "created_at": "2026-07-21T03:47:34+00:00", "title": "Fail-closed six-claim gate", "command": ["python", "repro/src/gate.py"], "exit_code": 0, "duration_s": 0.035}
-->
````bash
$ python repro/src/gate.py
````

exit 0 · 0.0s


````python title=gate.py
"""Fail-closed local six-claim gate; reports the source-experiment limitation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parents[2]


def load(name: str):
    return json.loads((ROOT / "outputs" / name).read_text())


def main() -> None:
    first, complexity, theorem = load("initial_verdict.json"), load("complexity.json"), load("theorem_audits.json")
    c2, c3, c4 = theorem["normality"], theorem["online_covariance"], theorem["global_convergence"]
    operation_counts = [row["inner_operation_bound"] for row in complexity["rows"]]
    operation_doubling = [operation_counts[i+1]/operation_counts[i] for i in range(len(operation_counts)-1)]
    claims = {
        "C1": min(operation_doubling) > 3.7 and max(operation_doubling) < 4.1 and "d^2" in complexity["claim"],
        "C2": c2["relative_covariance_error"] < .10 and c2["lyapunov_residual"] < 1e-12 and c2["minimum_qq_r2"] > .995,
        "C3": c3["checkpoints"][-1]["mean_estimate_relative_error"] < .10 and c3["fitted_error_slope"] < 0,
        "C4": c4["tau_condition_satisfied"] and max(r["maximum_final_over_initial"] for r in c4["rows"]) < .01,
        "C5": first["claim_5"]["max_recurrence_error"] < 1e-11 and first["claim_5"]["max_radius_excess"] < 1e-11,
        "C6": max(first["claim_6"]["exact_newton_error"], first["claim_6"]["unaccelerated_identity_error"], first["claim_6"]["lyapunov_special_case_error"]) < 1e-11,
    }
    result = {"claims": claims, "all_six_checked": all(claims.values()),
              "scope": "clean-room theorem instances; source d=20 table protocol remains unreproduced because its parameter approximation is not released",
              "source_protocol_pilot": "failed and retained in outputs/pilot.json"}
    (ROOT / "outputs" / "local_gate.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    if not result["all_six_checked"]:
        raise SystemExit("local six-claim gate failed")


if __name__ == "__main__":
    main()

````


````output
{
  "claims": {
    "C1": true,
    "C2": true,
    "C3": true,
    "C4": true,
    "C5": true,
    "C6": true
  },
  "all_six_checked": true,
  "scope": "clean-room theorem instances; source d=20 table protocol remains unreproduced because its parameter approximation is not released",
  "source_protocol_pilot": "failed and retained in outputs/pilot.json"
}

````
