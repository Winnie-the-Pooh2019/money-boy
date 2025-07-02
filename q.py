import numpy as np
import cvxpy as cp

def distribute_budget_qp(c, A, B, L=None):
    """
    Решает задачу:
        min_x ||A x - y||_2^2
        s.t. sum(x)=B, x>=L, x>=0

    где y = (c / sum(c)) * B.

    Параметры:
      c (np.array[n])    — «сырые» счётчики упоминаний проблем
      A (np.array[n×m])  — матрица покрытия проблем статьями
      B (float)          — общий бюджет
      L (np.array[m])    — нижние пороги (по умолчанию нули)

    Возвращает:
      x_opt (np.array[m]) — оптимальное распределение
      metrics (dict)      — MAE, RMSE, MaxErr, PercErrs (по проблемам)
    """
    n, m = A.shape
    # 1) Нижние пороги
    if L is None:
        L = np.zeros(m)
    # 2) Целевая «идеальная» нагрузка на проблемы
    y = (c / c.sum()) * B

    # 3) Переменная
    x = cp.Variable(m)

    # 4) Функция невязки по проблемам
    residuals = A @ x - y
    loss = cp.sum_squares(residuals)

    # 5) Ограничения
    constraints = [
        cp.sum(x) == B,
        x >= L,
        x >= 0
    ]

    # 6) Решаем QP
    prob = cp.Problem(cp.Minimize(loss), constraints)
    prob.solve(solver=cp.OSQP)

    x_opt = x.value
    # 7) Считаем метрики качества покрытия проблем
    e = A @ x_opt - y
    MAE    = np.mean(np.abs(e))
    RMSE   = np.sqrt(np.mean(e**2))
    MaxErr = np.max(np.abs(e))
    # Процентные ошибки для каждой проблемы
    PercErrs = (e / y) * 100

    metrics = {
        'MAE':    MAE,
        'RMSE':   RMSE,
        'MaxErr': MaxErr,
        'PercErrs': PercErrs
    }

    return x_opt, metrics

# --- Пример использования ---
if __name__ == "__main__":
    # Данные
    c = np.array([550, 145, 200, 300])
    A = np.array([
        [0.7, 0.3, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.8, 0, 0.2]
    ])
    B = 1000.0
    L = np.array([100, 200, 200])

    x_opt, metrics = distribute_budget_qp(c, A, B, L=L)

    print("Оптимальное распределение бюджетa:")
    for j, val in enumerate(x_opt, 1):
        print(f"  Статья {j}: {val:.2f}")

    print("\nМетрики покрытия проблем:")
    print(f"  MAE     = {metrics['MAE']:.2f}")
    print(f"  RMSE    = {metrics['RMSE']:.2f}")
    print(f"  MaxErr  = {metrics['MaxErr']:.2f}")
    print("  %Errors = ", np.round(metrics['PercErrs'], 1))
