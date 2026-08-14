# Source audit

## Primary paper source

Pinned source: [arXiv 2604.23436v2](https://arxiv.org/abs/2604.23436), downloaded from the official arXiv e-print endpoint on 2026-07-21. The source files were used locally but are excluded from the public Git tree by `.gitignore`.

| File | SHA-256 | Used for |
| --- | --- | --- |
| `source/main.tex` | `7367c080f52e561de567992e83dbfcaea7d642d9a4169f2bee7edc32c30e630e` | Algorithm 1; Lemma 3.6; Theorems 3.8, 4.3, 4.6; Proposition 4.4 |
| `source/appendix.tex` | `26c26967a7b4e7367016a7aade055fdd7cdf9e8eba85d03ba307e43bf6fbc236` | d=20/40 regression protocol, Kaczmarz/Gaussian sketches, `τ=5/10`, 200 runs |
| `source/table.tex` | `ef81335368569b0634295e1b8b4df505cf01d60ac57d7e6c0def86d15beb131b` | d=40 result layout |
| `source/figure.tex` | `ec3febfe6b614dee7966815903e3404133c68404b2de1bb1e158e47088f89448` | QQ and empirical protocol layouts |

No author GitHub repository, archive, or executable was found in the paper, OpenReview record, author page, or the source audit. The implementation here is clean-room and does not claim source-code equivalence.

## Missing empirical detail

The source's empirical parameter approximation for `μ/ν` is material to the d=20/40 experiment. The literal population calculation and pilot are retained in `outputs/pilot.json`; no hidden tuning is substituted to force table parity.
