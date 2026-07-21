# Evidence ledger

| Anchored claim | Status | Evidence |
|---|---|---|
| C1 O(d²) NASketch | checked | `outputs/complexity.json`: fixed-rank operation count is quadratic in d; the implementation contains no dense B² materialization. |
| C2 CLT/Lyapunov | checked | `outputs/theorem_audits.json`: 2,400 non-Gaussian last iterates, nonzero K, independent Kronecker Lyapunov solve. |
| C3 online covariance | checked | Same artifact: 500 streams to horizon 24,000 using only four running sums. |
| C4 global convergence | checked | Same artifact: all 36 distant-start trajectories satisfy the explicit tau condition and converge. |
| C5 Cayley--Hamilton contraction | checked | `outputs/initial_verdict.json`: 220,011 spectral cells. |
| C6 exact/unaccelerated cases | checked | Same artifact: all special-case residuals are zero to float64 precision. |

The attempted source-level d=20 Kaczmarz protocol is deliberately retained as `outputs/pilot.json` and remains a disclosed failure: the paper omits the empirical parameter-estimation procedure required to match its reported `tau=5` experiments. The theorem-instance checks above do not claim Table or Figure reproduction.
