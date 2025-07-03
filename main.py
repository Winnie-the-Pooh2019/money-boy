import cvxpy as cp
import numpy as np


def distribute_budget(n, m, c, B, L, A):
    """
    Распределяет бюджетные средства на основе частоты упоминаний проблем и нижних пороговых ограничений.

    Параметры:
    n (int): число проблем
    m (int): число статей расходов
    w (np.array): веса статей
    c (np.array): частоты упоминаний проблем
    B (float): общий бюджет
    L (np.array): нижние пороговые ограничения для статей расходов
    a (np.array): матрица коэффициентов связи между проблемами и статьями расходов

    Возвращает:
    np.array: оптимальное распределение бюджета по статьям расходов
    """

    # Переменные для оптимизации
    x = cp.Variable(m, nonneg=True)
    l = L / sum(L)

    # y = c / c.sum()
    y = c / c.sum() * B

    # Целевая функция
    mu = 0.2
    I = A @ x - y
    # I = A @ x * B - y

    loss = cp.sum_squares(I)
    reg_loss = cp.sum_squares(x)

    print(f'I = {I}')
    objective = cp.Minimize(loss)
    # objective = cp.Minimize(loss + mu * reg_loss)

    # Ограничения
    constraints = [
        cp.sum(x) == B,
        *[x[i] >= l[i] for i in range(m)],
    ]
    # Задача оптимизации
    problem = cp.Problem(objective, constraints)

    # Решение задачи
    problem.solve(solver=cp.ECOS)
    # problem.solve(verbose=True)

    # Проверка статуса решения
    if problem.status in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        x_v = x.value
        e = A @ x_v - y

        mae = np.mean(np.abs(e))
        mse = np.mean(e ** 2)
        rmse = np.sqrt(np.mean(e ** 2))

        return x_v, mae, mse, rmse
    else:
        return None


x = np.array([
    1, 2, 3
])

# Пример использования функции
n = 4  # число проблем
m = 3  # число статей расходов
c = np.array([550, 145, 200, 300])  # частоты упоминаний проблем
B = 1000.0  # общий бюджет
L = np.array([100, 200, 200])  # нижние пороговые ограничения

# Коэффициенты связи (пример)
a = np.array([
    [0.7, 0.3, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.5, 0.5],
    [0.8, 0, 0.2]
])


n = 6  # число проблем
m = 6  # число статей расходов
c = np.array([550, 145, 200, 300, 400, 500])  # частоты упоминаний проблем
B = 10000.0  # общий бюджет
L = np.array([500, 600, 700, 800, 900, 1000])  # нижние пороговые ограничения
# L = [l * 0 for l in L]  # нижние пороговые ограничения

# Коэффициенты связи (пример)
a = np.array([
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0],
])

v = np.array([
    0.4, 0.2, 0.3, 0.1
])

print(f'a = {a}')
print(f'x = {x.T}')
# print(f'ax = {a @ x.T}')

# Распределение бюджета
result, mae, mse, rmse = distribute_budget(n, m, c, B, L, a)

if result is not None:
    print("Оптимальное распределение бюджета:")
    # result *= B
    for j in range(m):
        print(f"Статья расходов {j + 1}: {result[j]:.2f}")

    # Вычисление ошибки
    print(f"Среднеквадратичная ошибка (mae): {mae / B:.2f}")
    print(f"Среднеквадратичная ошибка (mse): {mse:.4f}")
    print(f"Среднеквадратичная ошибка (rmse): {rmse:.2f}")
else:
    print("Задача не имеет оптимального решения.")
