# Claim 1


---
<!-- trackio-cell
{"type": "code", "id": "cell_cb053552b81c", "created_at": "2026-07-21T03:47:26+00:00", "title": "Dense fixed-rank complexity audit", "command": ["python", "repro/src/complexity.py"], "exit_code": 0, "duration_s": 0.336}
-->
````bash
$ python repro/src/complexity.py
````

exit 0 · 0.3s


````python title=complexity.py
"""Full dense-dimension complexity audit for Algorithm 1's inner step."""

from __future__ import annotations

import json
from pathlib import Path
import time
import numpy as np

from nasketch import nasketch


def median_seconds(fn, repeats: int) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return float(np.median(samples))


def main() -> None:
    rng = np.random.default_rng(260423436)
    rows = []
    # Dense d=32..512 is the real dense-matrix protocol, not a sparse proxy.
    for d in (32, 64, 128, 256, 512):
        A = rng.normal(size=(d, d))
        B = A.T @ A / d + np.eye(d)
        g = rng.normal(size=d)
        S = np.eye(d)[:, [d // 2]]
        # warm-up avoids measuring allocation/import overhead.
        nasketch(B, g, .15, .8, 1.6, [S])
        inner = median_seconds(lambda: nasketch(B, g, .15, .8, 1.6, [S]), 40)
        direct = median_seconds(lambda: np.linalg.solve(B, -g), 12)
        # Algorithm 1 line 6 uses two dense matvecs plus O(d) work for s=1.
        operation_bound = 2 * d * d + 6 * d + 1
        rows.append({"d": d, "inner_seconds": inner, "solve_seconds": direct,
                     "inner_operation_bound": operation_bound})
    log_d = np.log([r["d"] for r in rows])
    inner_slope = float(np.polyfit(log_d, np.log([r["inner_seconds"] for r in rows]), 1)[0])
    solve_slope = float(np.polyfit(log_d, np.log([r["solve_seconds"] for r in rows]), 1)[0])
    report = {"rows": rows, "inner_runtime_slope": inner_slope,
              "dense_solve_runtime_slope": solve_slope,
              "claim": "For s=1, Algorithm 1 requires two dense matrix-vector products and no dense matrix-matrix product: O(d^2) time and O(d^2) storage for B."}
    out = Path("outputs/complexity.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

````


````output
{
  "rows": [
    {
      "d": 32,
      "inner_seconds": 5.747948307543993e-05,
      "solve_seconds": 1.6200472600758076e-05,
      "inner_operation_bound": 2241
    },
    {
      "d": 64,
      "inner_seconds": 7.471954450011253e-05,
      "solve_seconds": 6.699899677187204e-05,
      "inner_operation_bound": 8577
    },
    {
      "d": 128,
      "inner_seconds": 0.00011908751912415028,
      "solve_seconds": 0.00012264249380677938,
      "inner_operation_bound": 33537
    },
    {
      "d": 256,
      "inner_seconds": 0.00028080609627068043,
      "solve_seconds": 0.0005339400377124548,
      "inner_operation_bound": 132609
    },
    {
      "d": 512,
      "inner_seconds": 0.0010208309395238757,
      "solve_seconds": 0.0036959705175831914,
      "inner_operation_bound": 527361
    }
  ],
  "inner_runtime_slope": 1.0211122816808402,
  "dense_solve_runtime_slope": 1.8662013412397405,
  "claim": "For s=1, Algorithm 1 requires two dense matrix-vector products and no dense matrix-matrix product: O(d^2) time and O(d^2) storage for B."
}

````
