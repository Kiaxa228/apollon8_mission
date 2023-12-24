import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import constants
import math

data_of_rocket = {
    "m0": 35947.0,
    "M": 128467,
    "Thrust": 2552723.2872371494,
    "Drag_coefficient": 0.5,
    "Atmospheric_Pressure": 1.29,
    "Section_area": 27.56,
    "g": 1.00034 * constants.g,
    "Fuel_consumption_coefficient": (128467 - 35947) / (160)
}


# На данном этапе мы симулируем полет ракеты определеняя функцию
def simulate(m0, M, Thrust, Drag_coefficient, Atmospheric_Pressure, Section_area, g, Fuel_consumption_coefficient, duration, num_points):
    v0 = 0

    t_mass = (0, duration)
    t_calc = np.linspace(*t_mass, num_points)

    rocket_args = (M, m0, Thrust, Drag_coefficient, Atmospheric_Pressure, Section_area, g, Fuel_consumption_coefficient)

    solve = integrate.solve_ivp(
        equations_calculations,
        t_span=t_mass,
        y0=[v0],
        t_eval=t_calc,
        args=rocket_args
    )  # Для нахождения скорости решаем дифференциальное уравнение

    return solve.t, solve.y[0]  # Возвращаем время и скорость, чтобы вывести время и скорость в графике


# Определяем функцию для уравнений ракеты
def equations_calculations(time, velocity, M, m0, Th, Cf, Dc, Sa, g, k):
    Ve = Th / (M - k * time) - (Cf * Dc * Sa) / (
            2 * (M - k * time)) * velocity ** 2  # Расчитываем параметры для изменения скорости сброса топлива
    dvdt = (math.log(m0 / (m0 - k * time)) - 0.5 * (Dc / (m0 - k))) * Ve  # Вычисляем производной скорости по времени
    return dvdt


# Симуляция полета
time_simulation, velocity = simulate(**data_of_rocket, duration=50, num_points=1080)

time = []
speed = []
height = []

with open('stats.csv') as file_in:
    for line in file_in:
        if line.strip() == '':
            continue

        data = line.split(',')

        if data[0] == 'Time':
            continue

        time.append(int(data[0]))
        speed.append(float(data[1]))
        height.append(float(data[6]))

# Наконец, строим график
plt.figure(figsize=(5, 4))
plt.plot(time_simulation, velocity, '-g', label="Математическая модель")
plt.plot(time[:51], speed[:51], label="Ksp")
plt.legend()
plt.grid(True)
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.title('Скорость и Время')
plt.show()