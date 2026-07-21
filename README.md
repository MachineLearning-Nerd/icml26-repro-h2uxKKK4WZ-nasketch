# Inference of Online Newton Methods with Nesterov's Accelerated Sketching

Clean-room reproduction for ICML 2026 paper `h2uxKKK4WZ` (arXiv:2604.23436v2).

The authors released paper source, figures, and tables but no executable implementation was located during the audit.  This repository implements Algorithm 1 directly from the paper and keeps source material under `source/`.  Evidence will be accepted only after all six anchored claims, independent checks, and negative controls pass at the declared scales.

Run the initial deterministic algebraic checks with:

```bash
python repro/src/verify.py --out outputs/initial_verdict.json
```

