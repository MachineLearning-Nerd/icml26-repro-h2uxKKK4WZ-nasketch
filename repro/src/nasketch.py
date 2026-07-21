"""Clean-room NumPy implementation of Algorithm 1 in arXiv:2604.23436."""

from __future__ import annotations

import numpy as np


def parameters(mu: float, nu: float) -> tuple[float, float, float]:
    """Equation (2.5): return alpha, beta, gamma."""
    gamma = 1.0 / np.sqrt(mu * nu)
    return 1.0 / (1.0 + gamma * nu), 1.0 - np.sqrt(mu / nu), gamma


def projection(B: np.ndarray, S: np.ndarray) -> np.ndarray:
    """BS(S'B²S)^†S'B, evaluated independently from the iteration."""
    BS = B @ S
    return BS @ np.linalg.pinv(BS.T @ BS) @ BS.T


def nasketch(B: np.ndarray, g: np.ndarray, alpha: float, beta: float,
             gamma: float, sketches: list[np.ndarray]) -> np.ndarray:
    """Literal Algorithm 1, outputting the approximate solution of B dx=-g."""
    z = np.zeros_like(g, dtype=float)
    v = np.zeros_like(g, dtype=float)
    for S in sketches:
        y = alpha * v + (1.0 - alpha) * z
        # Algorithm 1, line 6.  This is deliberately not ``projection``:
        # projection includes the final B only for the error transition Z.
        BS = B @ S
        omega = BS @ np.linalg.pinv(BS.T @ BS) @ S.T @ (B @ y + g)
        z = y - omega
        v = beta * v + (1.0 - beta) * y - gamma * omega
    return z


def G(alpha: float, beta: float, gamma: float, z: float) -> np.ndarray:
    """Equation (3.4), the two-by-two eigen-direction transition matrix."""
    return np.array([
        [1.0 - alpha, alpha],
        [(1.0-alpha)*(1.0-beta), alpha + beta - alpha*beta],
    ]) - z * np.array([
        [1.0-alpha, alpha],
        [(1.0-alpha)*gamma, alpha*gamma],
    ])


def ch_sequence(alpha: float, beta: float, gamma: float, z: float, steps: int) -> np.ndarray:
    """Cayley--Hamilton recurrence in Lemma 3.6, including p_0."""
    mat = G(alpha, beta, gamma, z)
    values = np.empty(steps + 1)
    values[0] = 1.0
    if steps:
        values[1] = 1.0 - z
    tr, det = np.trace(mat), np.linalg.det(mat)
    for k in range(2, steps + 1):
        values[k] = tr * values[k - 1] - det * values[k - 2]
    return values


def direct_sequence(alpha: float, beta: float, gamma: float, z: float, steps: int) -> np.ndarray:
    mat = G(alpha, beta, gamma, z)
    one = np.ones(2)
    e1 = np.array([1.0, 0.0])
    return np.array([e1 @ np.linalg.matrix_power(mat, k) @ one for k in range(steps + 1)])


def solve_lyapunov(A: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """Independent Kronecker solve of A X + X A' = Q."""
    d = A.shape[0]
    system = np.kron(np.eye(d), A) + np.kron(A, np.eye(d))
    return np.linalg.solve(system, Q.reshape(-1)).reshape(d, d)
