import numpy as np
import cvxpy as cp

def distribute_budget_lexico(A, v, B, L=None, epsilon=1e-3):
    """
    Распределение бюджета в два этапа:
      1) Минимизируем L2‑невязку покрытия проблем.
      2) При небольшом допуске по невязке «выжимаем» максимум использования бюджета.

    Параметры:
      A       np.array[n×m] — матрица покрытия "проблема→статья"
      v       np.array[n]   — счётчики упоминаний проблем
      B       float         — общий бюджет
      L       np.array[m]   — нижние пороги затрат по статьям (абсолютные), по умолчанию None→0
      epsilon float         — допустимое ухудшение первой задачи (в единицах квадратичной ошибки)

    Возвращает:
      z1      np.array[m] — распределение после первого этапа (использование ≤ B)
      z2      np.array[m] — распределение после второго этапа (финальное)
      metrics dict:
        cov1    — L2‑невязка первой фазы
        used1   — сумма z1 (обычно = B)
        cov2    — L2‑невязка второй фазы
        used2   — сумма z2
    """
    n, m = A.shape
    # Целевые абсолютные расходы по проблемам
    y = (v / v.sum()) * B

    # Нижние пороги на доли бюджета x_j = z_j / B
    if L is None:
        L = np.zeros(m)
    lb = L / B  # теперь ограничения x_j ≥ lb

    # Переменные для обоих этапов — доли бюджета
    x = cp.Variable(m)

    # Функция невязки покрытия (в абсолютных единицах)
    z = x * B
    cov_loss = cp.sum_squares(A @ z - y)  # = ||A·(xB) - y||²

    # Общие ограничения
    cons = [
        cp.sum(x) <= 1,
        x >= lb,
        x <= 1
    ]

    # --- Этап 1: минимизация невязки покрытия ---
    prob1 = cp.Problem(cp.Minimize(cov_loss), cons)
    prob1.solve(solver=cp.OSQP)

    if prob1.status != cp.OPTIMAL:
        raise RuntimeError(f"Первый этап не решил задачу: {prob1.status}")

    cov1  = cov_loss.value
    z1    = x.value * B
    used1 = z1.sum()

    # --- Этап 2: максимизация использования бюджета при допуске по невязке ---
    # Ограничение: cov_loss ≤ cov1 + epsilon
    cons2 = cons + [
        cov_loss <= cov1 + epsilon
    ]
    # Цель: максимизировать sum(z) = B * sum(x) => эквивалентно max sum(x)
    prob2 = cp.Problem(cp.Maximize(cp.sum(x)), cons2)
    prob2.solve()

    if prob2.status != cp.OPTIMAL:
        raise RuntimeError(f"Второй этап не решил задачу: {prob2.status}")

    cov2  = cov_loss.value
    z2    = x.value * B
    used2 = z2.sum()

    metrics = {
        'cov1':  cov1,
        'used1': used1,
        'cov2':  cov2,
        'used2': used2
    }
    return z1, z2, metrics


# --- Пример использования ---
if __name__ == "__main__":
    # Матрица покрытия (n проблем × m статей)
    A = np.array([
        [0.7, 0.3, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.8, 0.0, 0.2]
    ])
    v = np.array([550, 145, 200, 300])    # упоминания проблем
    B = 1000.0                            # общий бюджет
    L = np.array([100, 200, 200])        # нижние пороги по статьям

    # Запускаем лексикографию
    z1, z2, metrics = distribute_budget_lexico(A, v, B, L=L, epsilon=1e-2)

    # Выводим результаты
    print("Этап 1 (минимизация невязки):")
    print(" z1 =", np.round(z1, 2))
    print(f" Невязка = {metrics['cov1']:.2f}, Использовано = {metrics['used1']:.2f}")

    print("\nЭтап 2 (максимизация расхода при допуске):")
    print(" z2 =", np.round(z2, 2))
    print(f" Невязка = {metrics['cov2']:.2f}, Использовано = {metrics['used2']:.2f}")
