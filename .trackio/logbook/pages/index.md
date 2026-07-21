# Repro - Inference of Online Newton Methods with Nesterov's Accelerated Sketching

This clean-room CPU reproduction passes its local six-claim gate. It directly implements Algorithm 1 and independently audits its fixed-rank complexity, Lyapunov last-iterate limit, online covariance estimator, global convergence conditions, Cayley--Hamilton contraction, and exact/unaccelerated special cases. The author source includes paper figures and TeX but no executable protocol; the failed d=20/`tau=5` source-experiment attempt is retained and explicitly excluded from the theorem-instance claims.

## Pages

| Page |
| --- |
| [Claim 1](#/claim-1) |
| [Claims 2-4](#/claims-2-4) |
| [Claims 5-6](#/claims-5-6) |
| [Conclusion](#/conclusion) |
| [Tests](#/tests) |
