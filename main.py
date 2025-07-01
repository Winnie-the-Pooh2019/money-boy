import cvxpy as cp
import numpy as np


def distribute_budget(n, m, w, c, B, L, A, mu=0):
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
    # Идеальное распределение
    v = c / c.sum()

    # I = np.zeros(m)
    # I = B *
    # for j in range(m):
    #     I[j] = sum(a[i][j] * c[i] for i in range(n))

    # Переменные для оптимизации
    x = cp.Variable(m, nonneg=True)

    y = c / c.sum() * B

    # Целевая функция
    I = A @ x - y

    loss = cp.sum_squares(I)

    if mu > 0:
        loss_p = mu * cp.sum_squares(x - w * B)
    else:
        loss_p = 0

    print(f'I = {I}')
    objective = cp.Minimize(loss + loss_p)

    # Ограничения
    constraints = [
        cp.sum(x) == B,
        x >= L
    ]
    # генетические алгоритмы
    # обучение с подкреплением частота на стоимость среднюю - бюджет
    # Задача оптимизации
    problem = cp.Problem(objective, constraints)

    # Решение задачи
    problem.solve(solver=cp.OSQP)

    # Проверка статуса решения
    if problem.status == cp.OPTIMAL:
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

w = np.array([
    0.4, 0.3, 0.3
])

v = np.array([
    0.4, 0.2, 0.3, 0.1
])

print(f'ax = {a @ x}')

# Распределение бюджета
result, mae, mse, rmse = distribute_budget(n, m, w, c, B, L, a)

if result is not None:
    print("Оптимальное распределение бюджета:")
    for j in range(m):
        print(f"Статья расходов {j + 1}: {result[j]:.2f}")

    # Вычисление ошибки
    print(f"Среднеквадратичная ошибка (mae): {mae:.2f}")
    print(f"Среднеквадратичная ошибка (mse): {mse:.2f}")
    print(f"Среднеквадратичная ошибка (rmse): {rmse:.2f}")
else:
    print("Задача не имеет оптимального решения.")
