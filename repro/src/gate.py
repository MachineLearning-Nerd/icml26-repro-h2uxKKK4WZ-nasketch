"""Write the evidence-local gate for the six scoped NASketch audits."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load(name: str):
    return json.loads((ROOT / "outputs" / name).read_text())


def main() -> None:
    first = load("initial_verdict.json")
    complexity = load("complexity.json")
    theorem = load("theorem_audits.json")
    normality = theorem["normality"]
    covariance = theorem["online_covariance"]
    convergence = theorem["global_convergence"]
    operation_counts = [row["inner_operation_bound"] for row in complexity["rows"]]
    operation_doubling = [
        operation_counts[i + 1] / operation_counts[i]
        for i in range(len(operation_counts) - 1)
    ]
    claims = {
        "C1": min(operation_doubling) > 3.7 and max(operation_doubling) < 4.1 and "d^2" in complexity["claim"],
        "C2": normality["relative_covariance_error"] < 0.10 and normality["lyapunov_residual"] < 1e-12 and normality["minimum_qq_r2"] > 0.995,
        "C3": covariance["checkpoints"][-1]["mean_estimate_relative_error"] < 0.10 and covariance["fitted_error_slope"] < 0,
        "C4": convergence["tau_condition_satisfied"] and max(row["maximum_final_over_initial"] for row in convergence["rows"]) < 0.01,
        "C5": first["claim_5"]["max_recurrence_error"] < 1e-11 and first["claim_5"]["max_radius_excess"] < 1e-11,
        "C6": max(first["claim_6"]["exact_newton_error"], first["claim_6"]["unaccelerated_identity_error"], first["claim_6"]["lyapunov_special_case_error"]) < 1e-11,
    }
    assert all(claims.values())

    gate = {
        "schema_version": 2,
        "paper": {
            "openreview_id": "h2uxKKK4WZ",
            "title": "Inference of Online Newton Methods with Nesterov's Accelerated Sketching",
            "arxiv": "2604.23436v2",
        },
        "repository": {
            "owner": "MachineLearning-Nerd",
            "original_name": "icml26-repro-h2uxKKK4WZ-nasketch",
            "target_name": "icml26-inference-online-newton-nesterov-accelerated-sketching",
            "default_branch": "main",
        },
        "evidence_release_gate": "PASSED",
        "overall_status": "VERIFIED_SCOPED",
        "strict_paper_gate": "NOT_READY",
        "recorded_local_tests_passed": True,
        "substantive_claims": 6,
        "claims_verified_scoped": 6,
        "claims_falsified": 0,
        "claims_blocked": 0,
        "outcomes": {
            "VERIFIED_SCOPED": ["C1", "C2", "C3", "C4", "C5", "C6"],
            "FALSIFIED": [],
            "BLOCKED": [],
        },
        "claim_results": {
            "C1": "VERIFIED_SCOPED_COMPLEXITY",
            "C2": "VERIFIED_SCOPED_ASYMPTOTIC_NORMALITY",
            "C3": "VERIFIED_SCOPED_ONLINE_COVARIANCE",
            "C4": "VERIFIED_SCOPED_GLOBAL_CONVERGENCE",
            "C5": "VERIFIED_SCOPED_CAYLEY_HAMILTON",
            "C6": "VERIFIED_SCOPED_SPECIAL_CASES",
        },
        "empirical_protocol": {
            "status": "NOT_READY_MISSING_PARAMETER_APPROXIMATION",
            "failed_literal_pilot": "outputs/pilot.json",
            "table_figure_reproduction_claimed": False,
        },
        "publication": {
            "status": "PUBLIC_GITHUB_HANDOFF_ONLY",
            "external_score_claimed": False,
        },
        "scope": (
            "All six theorem-instance contracts pass. The paper's d=20/40 "
            "regression table and figure protocol remains unreproduced because "
            "the empirical parameter approximation is not released; the literal "
            "pilot is retained as negative evidence."
        ),
    }
    payload = json.dumps(gate, indent=2) + "\n"
    for output_path in (
        ROOT / "publication_gate.json",
        ROOT / "outputs/publication_gate.json",
        ROOT / "outputs/local_gate.json",
    ):
        output_path.write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
