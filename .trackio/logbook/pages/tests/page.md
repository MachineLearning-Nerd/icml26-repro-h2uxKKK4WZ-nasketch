# Tests


---
<!-- trackio-cell
{"type": "code", "id": "cell_3ca176a10262", "created_at": "2026-07-21T03:47:35+00:00", "title": "Unit tests", "command": ["python", "-m", "unittest", "discover", "-s", "repro/tests", "-v"], "exit_code": 0, "duration_s": 0.133}
-->
````bash
$ python -m unittest discover -s repro/tests -v
````

exit 0 · 0.1s


````output
test_cayley_hamilton_recurrence (test_nasketch.NASketchTests.test_cayley_hamilton_recurrence) ... ok
test_full_identity_sketch_is_exact_newton (test_nasketch.NASketchTests.test_full_identity_sketch_is_exact_newton) ... ok
test_lyapunov_kronecker_solution (test_nasketch.NASketchTests.test_lyapunov_kronecker_solution) ... ok
test_projection_is_idempotent (test_nasketch.NASketchTests.test_projection_is_idempotent) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK

````
