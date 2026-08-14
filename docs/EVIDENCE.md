# Evidence ledger

This ledger distinguishes scoped theorem-instance checks from the paper's unreproduced empirical regression protocol. `VERIFIED_SCOPED` means the declared local contract and its independent arithmetic checks pass; it does not claim author-code equivalence or table/figure parity.

## C1 — `O(d²)` NASketch complexity

`repro/src/complexity.py::main` evaluates dense matrices at `d=32,64,128,256,512`. For `s=1`, the implementation performs two dense matrix-vector products and linear work around them; the operation bound is `2d²+6d+1`, and the code never materializes dense `B²`. The recorded operation-count doublings are consistent with a quadratic bound.

Result: **VERIFIED_SCOPED**.

## C2 — last-iterate normality and Lyapunov covariance

`repro/src/theorem_audits.py::normality_audit` uses dimension 6, 2,400 independent last iterates, horizon 4,000, non-Gaussian centered exponential innovations, and a nonzero diagonal `K`. The relative covariance error is `.0731207362`, the Lyapunov residual is `5.55e-17`, and the minimum QQ `R²` is `.9976582849`.

Result: **VERIFIED_SCOPED** for this theorem-instance route.

## C3 — online covariance estimator

`covariance_audit` uses 500 independent dimension-3 streams and four running sums, with checkpoints through horizon 24,000. The final mean estimate relative error is `.0353443555`, and the fitted error slope is `-.0906114945`.

Result: **VERIFIED_SCOPED** for this finite online-estimation route.

## C4 — global convergence

`global_convergence_audit` evaluates 36 trajectories from initial radii 1, 10, and 100 on a strongly convex nonlinear objective. The explicit condition has lhs `.0428113612` and rhs `.078125`; all trajectories satisfy the condition and the largest final/initial ratio is `.0010536086`.

Result: **VERIFIED_SCOPED**.

## C5 — Cayley–Hamilton contraction

`repro/src/verify.py::main` checks 11 `(μ,ν)` parameter pairs, 20,001 spectral points each, and 64 recurrence steps. Across 220,011 cells, the maximum recurrence error is `7.0277e-14` and the maximum spectral-radius excess is `1.1102e-16`.

Result: **VERIFIED_SCOPED**.

## C6 — exact and special cases

The deterministic route checks the exact full-sketch Newton solve, the unaccelerated identity-sketch reduction, and the Lyapunov diagonal special case. All three residuals are zero at float64 precision.

Result: **VERIFIED_SCOPED**.

## Empirical protocol limitation

The paper's d=20/40 Kaczmarz/Gaussian regression experiment uses an empirical approximation of parameters such as `μ` and `ν`, but the procedure is not specified. The literal d=20/`τ=5` pilot in `outputs/pilot.json` gives `(α,β,γ)=(.0180,.9817,2.7279)` and diverges. This is retained as a failed reproduction attempt; it is not replaced by a different tuned procedure.

## Evidence path

```text
paper source anchor → clean-room implementation → deterministic/stochastic audit
→ raw JSON + unit tests → fail-closed publication gate
```
