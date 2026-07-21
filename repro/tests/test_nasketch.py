import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from nasketch import ch_sequence, direct_sequence, nasketch, projection, solve_lyapunov


class NASketchTests(unittest.TestCase):
    def test_full_identity_sketch_is_exact_newton(self):
        B = np.diag([1.0, 2.0, 4.0])
        g = np.array([1.0, -3.0, 2.0])
        got = nasketch(B, g, .5, 0.0, 1.0, [np.eye(3)])
        self.assertLess(np.max(np.abs(got + np.linalg.solve(B, g))), 1e-12)

    def test_projection_is_idempotent(self):
        B = np.diag([1.0, 2.0, 3.0])
        P = projection(B, np.eye(3)[:, [1]])
        self.assertLess(np.max(np.abs(P @ P-P)), 1e-12)

    def test_cayley_hamilton_recurrence(self):
        rec = ch_sequence(.2, .7, 1.5, .3, 64)
        direct = direct_sequence(.2, .7, 1.5, .3, 64)
        self.assertLess(np.max(np.abs(rec-direct)), 1e-11)

    def test_lyapunov_kronecker_solution(self):
        A = np.diag([.4, .7])
        Q = np.array([[2.0, .3], [.3, 1.0]])
        X = solve_lyapunov(A, Q)
        self.assertLess(np.max(np.abs(A @ X+X @ A.T-Q)), 1e-12)


if __name__ == "__main__":
    unittest.main()
