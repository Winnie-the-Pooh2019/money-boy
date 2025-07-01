import numpy as np
import cvxpy as cp

def allocate_budget_L2(w, A, B, L=None, p=None):
    """
    Распределение бюджета по L2‑критерию (взвешенные квадраты).

    Параметры:
    - w: np.array, размер n, веса проблем (сумма = 1).
    - A: np.array, размер n×m, матрица покрытия (строки нормированы).
    - B: float, общий бюджет.
    - L: np.array или None, размер m, нижние пороги (по умолчанию zeros).
    - U: np.array или None, размер m, верхние пороги (по умолчанию B).
    - p: np.array или None, размер n, приоритеты проблем (по умолчанию p = 1/n).

    Возвращает:
    - x_opt: np.array, оптимальное распределение бюджета (размер m).
    - metrics: dict с ключами 'R2', 'MAE', 'RMSE', 'MAEp', 'RMSEp'.


    """
    n, m = A.shape
    L = np.zeros(m) if L is None else L
    p = np.ones(n) / n if p is None else p

    # Целевые расходы по проблемам
    y = w * B

    # Переменная оптимизации
    x = cp.Variable(m)

    # Функция цели: взвешенные квадраты ошибок
    residuals = A @ x - y
    objective = cp.Minimize(cp.sum(cp.multiply(p, cp.square(residuals))))

    # Ограничения
    constraints = [
        cp.sum(x) == B,
        x >= L,
    ]

    # Решаем QP
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.OSQP)

    x_opt = x.value

    # Вычисляем ошибки
    e = A @ x_opt - y
    MAE = np.mean(np.abs(e))
    RMSE = np.sqrt(np.mean(e**2))
    MAEp = np.sum(p * np.abs(e))
    RMSEp = np.sqrt(np.sum(p * (e**2)))

    # R^2
    y_mean = np.mean(y)
    SS_res = np.sum(e**2)
    SS_tot = np.sum((y - y_mean)**2)
    R2 = 1 - SS_res / SS_tot if SS_tot > 0 else np.nan

    if prob.status == cp.OPTIMAL:
        metrics = {
            'R2': R2,
            'MAE': MAE,
            'RMSE': RMSE,
            'MAEp': MAEp,
            'RMSEp': RMSEp
        }

        return x_opt, metrics
    else:
        return None


# Пример использования:
if __name__ == "__main__":
    # Примерные данные
    n, m = 5, 4
    w = np.array([0.1, 0.2, 0.3, 0.25, 0.15])
    A = np.random.dirichlet(np.ones(m), size=n)
    B = 1000.0
    L = np.zeros(m) * 100
    U = np.ones(m) * 100

    x_opt, metrics = allocate_budget_L2(w, A, B, L)
    print("Оптимальное распределение:", x_opt)
    print("Метрики качества:", metrics)
