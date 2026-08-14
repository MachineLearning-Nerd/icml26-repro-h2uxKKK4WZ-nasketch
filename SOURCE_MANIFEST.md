# Source manifest

## Paper

- Title: *Inference of Online Newton Methods with Nesterov's Accelerated Sketching*
- Authors: Haoxuan Wang; Xinchen Du; Sen Na
- arXiv: [2604.23436v2](https://arxiv.org/abs/2604.23436)
- OpenReview identifier: `h2uxKKK4WZ`
- Accepted at ICML 2026
- Source archive: downloaded locally on 2026-07-21; excluded from public tree by `.gitignore`

## Claim anchors

| Claim | Primary source anchor | Local producer | Output |
| --- | --- | --- | --- |
| C1 | Algorithm 1 complexity discussion | `repro/src/complexity.py::main` | `outputs/complexity.json` |
| C2 | asymptotic normality and Lyapunov covariance | `repro/src/theorem_audits.py::normality_audit` | `outputs/theorem_audits.json` |
| C3 | online covariance estimator | `repro/src/theorem_audits.py::covariance_audit` | `outputs/theorem_audits.json` |
| C4 | global convergence theorem | `repro/src/theorem_audits.py::global_convergence_audit` | `outputs/theorem_audits.json` |
| C5 | Lemma 3.6 / spectral contraction | `repro/src/verify.py::main` | `outputs/initial_verdict.json` |
| C6 | exact and unaccelerated special cases | `repro/src/verify.py::main` | `outputs/initial_verdict.json` |

## Repository provenance

- Original repository: `MachineLearning-Nerd/icml26-repro-h2uxKKK4WZ-nasketch`
- Original audited tip: `c4cb876a279b0bb8f7d8bfba547ed5dc581f093c`
- Target repository: `MachineLearning-Nerd/icml26-inference-online-newton-nesterov-accelerated-sketching`
- Target default branch: `main`
- Final attribution: `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`
