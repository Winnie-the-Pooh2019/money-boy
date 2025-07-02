import numpy as np
from scipy.optimize import linprog

def distribute_budget_L1_lp(A, v, B, L=None):
    """
    Распределение бюджета L1‑методом (LP).

    Параметры:
      A  — матрица размер n×m
      v  — вектор длинны n (сырые упоминания проблем)
      B  — скаляр (общий бюджет)
      L  — вектор нижних порогов длины m (если None — нули)

    Возвращает:
      x_opt — оптимальный вектор бюджета длины m
      eps   — вектор ошибок длины n
    """
    n, m = A.shape
    if L is None:
        L = np.zeros(m)

    # Целевая нагрузка по проблемам
    y = (v / v.sum()) * B

    # Переменные: сначала x[0..m-1], потом eps[m..m+n-1]
    # Всего m + n переменных
    # Целевая функция: min sum eps_i -> c = [0,...,0, 1,...,1]
    c_vec = np.hstack([np.zeros(m), np.ones(n)])

    # Ограничения равенства: sum_j x_j = B
    A_eq = np.hstack([np.ones((1, m)), np.zeros((1, n))])
    b_eq = np.array([B])

    # Неравенства:
    # Для каждой i:
    #   A[i]·x - eps[i] <= y[i]
    #  -A[i]·x - eps[i] <= -y[i]
    A_ub = []
    b_ub = []

    # A[i]·x - eps[i] <= y[i]
    for i in range(n):
        row = np.hstack([ A[i], np.zeros(n) ])
        row[m + i] = -1
        A_ub.append(row)
        b_ub.append(y[i])

    # -A[i]·x - eps[i] <= -y[i]
    for i in range(n):
        row = np.hstack([ -A[i], np.zeros(n) ])
        row[m + i] = -1
        A_ub.append(row)
        b_ub.append(-y[i])

    A_ub = np.vstack(A_ub)
    b_ub = np.array(b_ub)

    # Границы для x и eps
    bounds = []
    # x_j >= L_j
    for j in range(m):
        bounds.append((L[j], None))
    # eps_i >= 0
    for i in range(n):
        bounds.append((0, None))

    # Решаем LP
    res = linprog(c=c_vec,
                  A_ub=A_ub, b_ub=b_ub,
                  A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds,
                  method='highs')

    if not res.success:
        raise RuntimeError("LP не решилась: " + res.message)

    x_opt = res.x[:m]
    eps   = res.x[m:]
    return x_opt, eps

# --- Пример использования ---
if __name__ == "__main__":
    # Данные
    A = np.array([
        [0.7, 0.3, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.8, 0, 0.2]
    ])
    v = np.array([550, 145, 200, 300])
    B = 1000.0
    L = np.array([100, 200, 200])

    x_opt, eps = distribute_budget_L1_lp(A, v, B, L)

    # Метрики покрытия проблем
    y = (v / v.sum()) * B
    cover = A @ x_opt
    errors = cover - y

    RMSE = np.sqrt(np.mean(errors**2))
    MAE  = np.mean(np.abs(errors))
    MaxE = np.max(np.abs(errors))

    print("x_opt =", np.round(x_opt,2))
    print("cover =", np.round(cover,2))
    print("RMSE =", RMSE)
    print("MAE  =", MAE)
    print("MaxE =", MaxE)
