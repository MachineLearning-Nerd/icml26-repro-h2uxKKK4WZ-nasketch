# Status — Inference of Online Newton Methods with Nesterov's Accelerated Sketching

## Current release

- Repository target: `MachineLearning-Nerd/icml26-inference-online-newton-nesterov-accelerated-sketching`
- Paper: *Inference of Online Newton Methods with Nesterov's Accelerated Sketching*
- OpenReview: `h2uxKKK4WZ`
- arXiv: `2604.23436v2`
- Evidence release gate: **PASSED**
- Overall result: **VERIFIED_SCOPED**
- Strict paper-level gate: **NOT_READY**
- External score claimed: **no**
- Author executable implementation found: **no**
- Paper empirical parameter-approximation procedure: **MISSING**

## Claim status

| Claim | Final status | Scope |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | Dense `s=1` operation-count and storage audit |
| C2 | `VERIFIED_SCOPED` | Non-Gaussian last-iterate normality and Lyapunov covariance instance |
| C3 | `VERIFIED_SCOPED` | 500-stream online covariance route through horizon 24,000 |
| C4 | `VERIFIED_SCOPED` | 36 global-convergence trajectories under explicit `τ` condition |
| C5 | `VERIFIED_SCOPED` | 220,011-cell Cayley–Hamilton and spectral audit |
| C6 | `VERIFIED_SCOPED` | Exact, unaccelerated, and Lyapunov special cases |

## Recorded evidence

- C1: operation-count ratio is quadratic across `d=32..512`; no dense matrix-matrix product is used in the `s=1` inner step
- C2: 2,400 last iterates; relative covariance error `.0731207362`; minimum QQ `R²=.9976582849`
- C3: 500 streams; maximum horizon `24,000`; final relative error `.0353443555`; fitted slope `-.0906114945`
- C4: 36 trajectories; `τ=24`; condition lhs `.0428113612` ≤ rhs `.078125`; largest final/initial ratio `.0010536086`
- C5: 220,011 spectral cells; maximum recurrence error `7.0277e-14`; radius excess `1.1102e-16`
- C6: exact Newton error `0`; unaccelerated identity error `0`; Lyapunov special-case error `0`
- Negative evidence: literal d=20/`τ=5` Kaczmarz pilot diverges because the source's empirical `μ/ν` approximation is unspecified

## Reproduction boundary

The paper source tarball is pinned and was used locally, but `source/` is ignored and absent from the public clone. No author code was found. The theorem-instance checks are self-contained; the reported regression tables and figures remain unreproduced until the missing parameter-approximation procedure is recovered.
