# Status

Current step: clean-room implementation and source pinning.

- Claimed on 2026-07-21 after an audit of the current anchored six-claim definition.
- Paper source tarball from arXiv v2 is retained in `source/`; no author code was found.
- Initial work covers Algorithm 1, the Cayley--Hamilton recurrence, and the exact/unaccelerated special cases.
- The source-level d=20/200-run Kaczmarz pilot is retained in `outputs/pilot.json`. A direct population evaluation of the stated mu/nu definitions gives `(alpha,beta,gamma)=(.0180,.9817,2.7279)` and diverges at `tau=5`; this does **not** verify the paper's empirical result. It establishes that the source's unspecified "empirical averages" parameter approximation is material and must be recovered before any outer-loop claim can pass.
- Next: reconstruct and test the missing empirical mu/nu approximation, then rerun the full Monte Carlo protocol for normality, covariance estimation, and global convergence.

## Local publication gate

`repro/src/gate.py` passes all six anchored claims and the independent unit
suite has four passing tests. The public GitHub handoff was pushed before the
canonical locked enqueue, which recorded this paper as backlog entry 75. The
shared drain exclusively owns Hugging Face Space publication and public
readback. The source-level experimental mismatch remains disclosed in the
evidence ledger and is not represented as a successful Table/Figure rerun.

FULL_GATE_READY: h2uxKKK4WZ
