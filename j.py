import numpy as np
import cvxpy as cp

def distribute_budget_L1(c, A, B, L=None, w=None, p=None):
    """
    Распределение бюджета методом L1 (минимизация суммы абсолютных отклонений).

    Параметры:
      c (np.array[n])      : счётчики упоминаний проблем
      A (np.array[n×m])    : матрица покрытия проблем статьями расходов
      B (float)            : общий бюджет
      L (np.array[m])      : нижние пороги по статьям (по умолчанию 0)
      w (np.array[m])      : приоритеты статей (используются только для регуляризации; по умолчанию None)
      p (np.array[n])      : веса проблем (по умолчанию равномерные)

    Возвращает:
      x_opt (np.array[m])  : оптимальное распределение бюджета
      metrics (dict)       : {'R2','MAE','RMSE','MAEp','RMSEp','SAE'}
                             где SAE = суммарная абсолютная ошибка = sum |e_i|
    """
    # Размерности
    n, m = A.shape

    # Пороги и веса
    L = np.zeros(m) if L is None else L
    p = np.ones(n)/n     if p is None else p

    # Целевой вектор абсолютных расходов по проблемам
    y = (c / c.sum()) * B    # размер n

    # Переменные: x_j >= 0  и  ε_i >= 0
    x   = cp.Variable(m, nonneg=True)
    eps = cp.Variable(n, nonneg=True)

    # Основная часть: для каждой проблемы |(A x)_i - y_i| <= ε_i
    residuals = A @ x - y    # размер n

    constraints = [
        cp.sum(x) == B,
        x >= L,
        residuals <=  eps,
        -residuals <=  eps
    ]

    # Целевая функция: минимизировать взвешенную сумму ε_i
    objective = cp.Minimize(cp.sum(cp.multiply(p, eps)))

    # Решаем LP
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.OSQP)  # или любым LP‑солвером

    x_opt = x.value
    e     = (A @ x_opt) - y   # ошибки по проблемам, размер n

    # Метрики качества
    SAE   = np.sum(np.abs(e))
    MAE   = np.mean(np.abs(e))
    RMSE  = np.sqrt(np.mean(e**2))
    MAEp  = np.sum(p * np.abs(e))
    RMSEp = np.sqrt(np.sum(p * e**2))

    # R^2
    SS_res = np.sum(e**2)
    SS_tot = np.sum((y - y.mean())**2)
    R2     = 1 - SS_res/SS_tot if SS_tot>0 else np.nan

    metrics = {
        'SAE':   SAE,
        'MAE':   MAE,
        'RMSE':  RMSE,
        'MAEp':  MAEp,
        'RMSEp': RMSEp,
        'R2':    R2
    }

    return x_opt, metrics

# --- Пример использования ---
if __name__ == "__main__":
    # Задаём данные
    c = np.array([550, 145, 200, 300])
    A = np.array([
        [0.7, 0.3, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.8, 0, 0.2]
    ])
    B = 1000.0
    # L = np.array([100, 200, 200])
    L = np.zeros(3)
    # равновероятные приоритеты проблем и статей
    p = np.ones(len(c))/len(c)
    w = np.ones(A.shape[1])/A.shape[1]

    x_opt, metrics = distribute_budget_L1(c, A, B, L=L, w=w, p=p)
    print("x_opt =", np.round(x_opt, 2))
    print("Metrics:", {k: round(v,2) for k,v in metrics.items()})
