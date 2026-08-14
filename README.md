# ICML 2026 — Inference of Online Newton Methods with Nesterov's Accelerated Sketching

Clean-room theorem-instance reproduction for [*Inference of Online Newton Methods with Nesterov's Accelerated Sketching*](https://arxiv.org/abs/2604.23436) by Haoxuan Wang, Xinchen Du, and Sen Na.

The paper studies online Newton methods whose Newton directions are approximated with a sketch-and-project solver and Nesterov acceleration. It develops an `O(d²)` update route, establishes global convergence, asymptotic normality with a Lyapunov covariance, an online covariance estimator, and special-case links to exact and unaccelerated Newton methods.

## Reproduction result

The local evidence gate passes all six scoped claim contracts. The strict paper-level gate remains **NOT_READY** because the paper's empirical parameter-approximation procedure for the reported regression tables and figures was not released. The attempted literal pilot is retained as negative evidence.

| Claim | Paper statement | Result | How the result is produced |
| --- | --- | --- | --- |
| C1 | Algorithm 1 has `O(d²)` inner-step cost and `O(d²)` storage for dense `B` when `s=1` | **VERIFIED_SCOPED** | `repro/src/complexity.py`; operation counts across `d=32..512` follow quadratic doubling and no dense `B²` is formed |
| C2 | Last-iterate asymptotic normality with Lyapunov covariance | **VERIFIED_SCOPED** | `repro/src/theorem_audits.py::normality_audit`; 2,400 non-Gaussian last iterates, relative covariance error `.073121`, QQ `R²≥.997658` |
| C3 | Fully online covariance estimation converges | **VERIFIED_SCOPED** | `repro/src/theorem_audits.py::covariance_audit`; 500 streams to horizon 24,000, final relative error `.035344`, fitted error slope `-.090612` |
| C4 | Global convergence under the stated `τ` condition | **VERIFIED_SCOPED** | `repro/src/theorem_audits.py::global_convergence_audit`; 36 trajectories from radii 1, 10, and 100, all satisfying the condition |
| C5 | Cayley–Hamilton recurrence and spectral contraction | **VERIFIED_SCOPED** | `repro/src/verify.py`; 220,011 spectral cells, maximum recurrence error `7.03e-14` and radius excess `1.11e-16` |
| C6 | Exact, unaccelerated, and Lyapunov special cases reduce as stated | **VERIFIED_SCOPED** | `repro/src/verify.py`; all three residuals are zero to float64 precision |

These outcomes are scoped to the explicit theorem and algebra contracts above. They do not claim that the paper's unreleased d=20/40 Kaczmarz regression protocol or its reported tables and figures were reproduced.

## Source and reproduction boundary

The original local audit pinned the arXiv v2 source tarball and recorded hashes for `main.tex`, `appendix.tex`, `table.tex`, and `figure.tex`. The source directory is ignored by `.gitignore` and is **not present in this public GitHub handoff**. No author executable implementation was found during the source audit.

The failed pilot in `outputs/pilot.json` uses the literal source definitions at `d=20`, `τ=5`, 12 runs, and 200 steps. Direct population evaluation gives `(α, β, γ)=(.0180, .9817, 2.7279)` and diverges. The paper's phrase “empirical averages” does not specify the missing approximation procedure, so the pilot is not relabeled as a successful table reproduction.

## Claim production map

| Claim | Producer | Recorded artifact | Evidence/control |
| --- | --- | --- | --- |
| C1 | `repro/src/complexity.py::main` | `outputs/complexity.json` | Dense dimensions `32,64,128,256,512`; operation-count ratios near four |
| C2 | `repro/src/theorem_audits.py::normality_audit` | `outputs/theorem_audits.json` | Centered exponential innovations, independent last iterates, Lyapunov solve, QQ audit |
| C3 | `repro/src/theorem_audits.py::covariance_audit` | `outputs/theorem_audits.json` | Four running sums only; checkpoints through horizon `24,000` |
| C4 | `repro/src/theorem_audits.py::global_convergence_audit` | `outputs/theorem_audits.json` | Explicit `τ` condition and 36 distant-start trajectories |
| C5 | `repro/src/verify.py::main` | `outputs/initial_verdict.json` | 11 parameter pairs × 20,001 spectral points × 64 recurrence steps |
| C6 | `repro/src/verify.py::main` | `outputs/initial_verdict.json` | Exact Newton, unaccelerated identity, and Lyapunov residual checks |

`repro/src/gate.py` reads the recorded artifacts, checks all six scoped contracts, and writes the consistent publication gate. The raw theorem-instance results and failed pilot remain available for inspection.

## Branch map

The original repository had one branch only. It is retained as the canonical `main` branch.

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Canonical source audit, clean-room implementation, evidence, and release metadata |

## Reproduce the scoped checks

The public implementation needs Python 3.12 and NumPy. The source archive is not required for the executable theorem-instance checks, but is required to independently inspect the exact paper anchors.

```bash
python repro/src/complexity.py
python repro/src/theorem_audits.py --out outputs/theorem_audits.json
python repro/src/verify.py --out outputs/initial_verdict.json
python repro/src/gate.py
python -m unittest discover -s repro/tests -v
```

Supporting documents:

- [Evidence ledger](docs/EVIDENCE.md)
- [Source audit](docs/SOURCE_AUDIT.md)
- [Source manifest and citation](SOURCE_MANIFEST.md)
- [Audit report](AUDIT_REPORT.md)
- [Branch audit](BRANCH_AUDIT.md)
- [Publication gate](publication_gate.json)

## Paper citation

```bibtex
@article{wang2026inference,
  title={Inference of Online Newton Methods with Nesterov's Accelerated Sketching},
  author={Wang, Haoxuan and Du, Xinchen and Na, Sen},
  journal={arXiv preprint arXiv:2604.23436},
  year={2026},
  note={ICML 2026}
}
```

Paper page: [arXiv:2604.23436v2](https://arxiv.org/abs/2604.23436). OpenReview identifier: `h2uxKKK4WZ`.

## Thank you

Thank you to Haoxuan Wang, Xinchen Du, and Sen Na for presenting a useful bridge between efficient online Newton updates and statistical inference, and for making the theoretical recurrence and covariance targets precise enough for an independent audit. This repository keeps the missing empirical procedure and its failed literal pilot visible.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
