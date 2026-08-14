# Repository audit report

## Decision

This repository is ready for a scoped theorem-instance evidence release. Its overall status is **VERIFIED_SCOPED**:

- all six declared local claim contracts pass;
- the implementation is clean-room because no author executable was found;
- the paper's empirical d=20/40 parameter-approximation procedure is missing;
- the literal pilot using the source's visible definitions diverges and is retained as negative evidence;
- no external score or table/figure reproduction is claimed.

## Paper summary

The paper proposes NASketch, an online Newton method whose approximate Newton direction is produced by sketch-and-project updates with Nesterov acceleration. The theory covers computational cost, global convergence, last-iterate normality, Lyapunov covariance, an online covariance estimator, and reductions to exact/unaccelerated Newton special cases.

## Claim-to-evidence decision

| Claim | Decision | Evidence |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | Quadratic dense operation audit with no dense `B²` construction |
| C2 | `VERIFIED_SCOPED` | 2,400 non-Gaussian last iterates and independent Lyapunov solve |
| C3 | `VERIFIED_SCOPED` | 500 online covariance streams through horizon 24,000 |
| C4 | `VERIFIED_SCOPED` | 36 convergence trajectories under the explicit `τ` condition |
| C5 | `VERIFIED_SCOPED` | 220,011 exact spectral/recurrence cells |
| C6 | `VERIFIED_SCOPED` | Exact, unaccelerated, and Lyapunov special-case identities |

## Reproduction boundary

The theorem-instance routes are self-contained in `repro/`. The empirical regression tables and figures are not reproduced because the source's empirical parameter approximation is unspecified. The failed literal pilot remains in `outputs/pilot.json`; it is not converted into a pass by selecting a hidden tuning rule.

## Gate state

- Evidence release gate: **PASSED**
- Overall status: **VERIFIED_SCOPED**
- Strict paper-level gate: **NOT_READY**
- Scoped verified claims: `6/6`
- Falsified claims: `0/6`
- Blocked claims: `0/6`
- External score claimed: **no**
