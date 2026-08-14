# Publication gate

## Final state

- Evidence release gate: **PASSED**
- Overall status: **VERIFIED_SCOPED**
- Strict paper-level gate: **NOT_READY**
- Scoped verified claims: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`
- Falsified claims: none
- Blocked claims: none
- Empirical table/figure reproduction: **NOT_READY** because the parameter-approximation procedure is unreleased
- External score claimed: **no**

Run the recorded scoped gate with:

```bash
python repro/src/complexity.py
python repro/src/theorem_audits.py --out outputs/theorem_audits.json
python repro/src/verify.py --out outputs/initial_verdict.json
python repro/src/gate.py
```
