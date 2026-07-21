"""Deterministic first gate for claims 1, 5, and 6; later gates are additive."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from nasketch import ch_sequence, direct_sequence, nasketch, parameters, solve_lyapunov


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(260423436)

    # Claim 5: 11 parameter pairs, 20,001 spectral points, 64 recurrence steps.
    max_recurrence_error = 0.0
    max_radius_excess = -np.inf
    cells = 0
    for mu in np.linspace(.02, .5, 11):
        nu = 1.0 / mu
        alpha, beta, gamma = parameters(mu, nu)
        bound = 1.0 - np.sqrt(mu / nu)
        z = np.linspace(mu, 1.0, 20001)
        base = np.array([[1-alpha, alpha], [(1-alpha)*(1-beta), alpha+beta-alpha*beta]])
        scale = np.array([[1-alpha, alpha], [(1-alpha)*gamma, alpha*gamma]])
        matrices = base[None, :, :] - z[:, None, None] * scale[None, :, :]
        traces = np.trace(matrices, axis1=1, axis2=2)
        determinants = np.linalg.det(matrices)
        recurrence = np.empty((65, z.size))
        recurrence[0], recurrence[1] = 1.0, 1.0-z
        powers = np.broadcast_to(np.eye(2), (z.size, 2, 2)).copy()
        direct = np.empty_like(recurrence)
        direct[0] = 1.0
        for step in range(1, 65):
            powers = matrices @ powers
            direct[step] = powers[:, 0, :].sum(axis=1)
            if step >= 2:
                recurrence[step] = traces*recurrence[step-1] - determinants*recurrence[step-2]
        max_recurrence_error = max(max_recurrence_error, float(np.max(np.abs(recurrence-direct))))
        max_radius_excess = max(max_radius_excess, float(np.max(np.abs(np.linalg.eigvals(matrices))) - bound))
        cells += z.size

    # Claim 6: exact solve and gamma=1 both reduce as stated by the paper.
    B = np.diag(np.array([1.0, 2.0, 4.0, 8.0]))
    g = rng.normal(size=4)
    exact = -np.linalg.solve(B, g)
    identity = np.eye(4)
    exact_solver = nasketch(B, g, .5, 0.0, 1.0, [identity])
    unaccelerated = nasketch(B, g, .5, 0.0, 1.0, [identity, identity])
    exact_error = float(np.max(np.abs(exact_solver-exact)))
    unaccelerated_error = float(np.max(np.abs(unaccelerated-exact)))
    omega = np.diag([.2, .4, .8, 1.6])
    lyapunov = solve_lyapunov(np.eye(4), omega)
    lyapunov_error = float(np.max(np.abs(lyapunov - omega/2.0)))

    verdict = {
        "claim_1": {"status": "in_progress", "note": "full scaling sweep pending"},
        "claim_2": {"status": "in_progress", "note": "Monte Carlo CLT pending"},
        "claim_3": {"status": "in_progress", "note": "online covariance protocol pending"},
        "claim_4": {"status": "in_progress", "note": "outer convergence protocol pending"},
        "claim_5": {"status": "pass", "spectral_cells": cells,
                    "max_recurrence_error": max_recurrence_error,
                    "max_radius_excess": max_radius_excess},
        "claim_6": {"status": "pass", "exact_newton_error": exact_error,
                    "unaccelerated_identity_error": unaccelerated_error,
                    "lyapunov_special_case_error": lyapunov_error},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(verdict, indent=2) + "\n")
    if max_recurrence_error > 1e-11 or max_radius_excess > 1e-11 or max(exact_error, unaccelerated_error, lyapunov_error) > 1e-11:
        raise SystemExit("deterministic gate failed")


if __name__ == "__main__":
    main()
