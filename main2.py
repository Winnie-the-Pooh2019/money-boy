import cvxpy as cp
import numpy as np


def distribute_budget_biobj(A, v, B, L=None, lambd=1.0):
    """
    Bi-objective via weighted sum:
      min  sum((B*A*x - y)^2) - lambd * B * sum(x)
      s.t. sum(x) <= 1, x >= L/B
    """
    n, m = A.shape
    y = (v / v.sum()) * B

    # Переменные: x in [L/B, 1]
    if L is None:
        L = np.zeros(m)
    lb = L / B

    x = cp.Variable(m)
    cov_loss = cp.sum_squares(B * (A @ x) - y)
    use_loss = -B * cp.sum(x)

    objective = cp.Minimize(cov_loss + lambd * use_loss)
    constraints = [
        cp.sum(x) <= 1,
        x >= lb,
        x <= 1
    ]

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.OSQP)

    x_opt = x.value
    z_opt = x_opt * B

    # Вычисляем метрики покрытия
    e = A @ z_opt - y
    rmse = np.sqrt(np.mean(e ** 2))
    used = z_opt.sum()

    return z_opt, rmse, used


# --- Пример использования ---
if __name__ == "__main__":
    A = np.array([
        [0.7, 0.3, 0],
        [0, 1, 0],
        [0, 0.5, 0.5],
        [0.8, 0, 0.2]
    ])
    v = np.array([550, 145, 200, 300])
    B = 1000.0
    L = np.array([100, 200, 200])

    for lambd in [0, 0.1, 1, 10]:
        z, rmse, used = distribute_budget_biobj(A, v, B, L=L, lambd=lambd)
        print(f"λ={lambd}: RMSE={rmse:.1f}, Used={used:.1f}")
        print(" z =", np.round(z, 1))
