from __future__ import annotations

from typing import TypedDict

import numpy as np
import numpy.typing as npt

from params import params
from policies import InterestRateStrategy


class ScenarioResult(TypedDict):
    """
    Результат ``simulate_scenario``: ряды длины N по кварталам.

    - ``quarters`` — индексы кварталов (0 … N-1).
    - ``inflation``, ``i_nom``, ``r_real`` — в % годовых (модель умножена на 100).
    - ``*_gdp`` — уровни ВВП, индекс (база 100 в t=0).
    - ``annual_losses``, ``cum_losses`` — потери в п.п. (модель ×100).
    """

    quarters: npt.NDArray[np.int_]
    inflation: npt.NDArray[np.float64]
    actual_gdp: npt.NDArray[np.float64]
    potential_gdp: npt.NDArray[np.float64]
    balanced_gdp: npt.NDArray[np.float64]
    i_nom: npt.NDArray[np.float64]
    r_real: npt.NDArray[np.float64]
    annual_losses: npt.NDArray[np.float64]
    cum_losses: npt.NDArray[np.float64]


def simulate_scenario(strategy: InterestRateStrategy) -> ScenarioResult:
    """
    Квартальная симуляция по модели из приложения 4 (Банк России).

    Выбор номинальной ставки делегируется переданной стратегии:
    ``i_nom[t] = strategy.get_interest_rate(t, pi, x)``.
    """
    N = 29
    pi = np.zeros(N)
    x = np.zeros(N)
    pi_e = np.zeros(N)
    i_nom = np.zeros(N)
    r_real = np.zeros(N)
    y_n = np.zeros(N)
    y_growth = np.zeros(N)          # темп роста ВВП (YoY) для расчёта потерь
    annual_losses = np.zeros(N)
    cum_losses = np.zeros(N)

    # === НОВОЕ: уровни ВВП (индекс 100 в t=0) ===
    actual_gdp = np.zeros(N)        # реальный ВВП (чёрная линия)
    potential_gdp = np.zeros(N)     # потенциальный ВВП (красная пунктирная)
    balanced_gdp = np.zeros(N)      # траектория сбалансированного роста (серая пунктирная)

    # Начальные условия (точно как в статье)
    pi[0] = 0.06
    x[0] = 0.01
    pi_e[0] = 0.06
    i_nom[0] = 0.16
    r_real[0] = (1 + 0.16) / (1 + 0.06) - 1
    y_n[0] = params['y0']
    y_growth[0] = 0.02 + (x[0] - 0.01)

    actual_gdp[0] = 100
    potential_gdp[0] = 100
    balanced_gdp[0] = 100

    x_past = np.full(4, 0.01)

    for t in range(1, N):
        # 1. Кривая Филлипса
        pi[t] = pi[t-1] + params['kappa1'] * x[t-1] + params['kappa2'] * x[t-1]**2

        # 2. Адаптация ожиданий
        lambda_t = params['lambda0'] + params['lambda1'] * (pi[t-1] - params['pi_T'])
        pi_e[t] = pi_e[t-1] + lambda_t * (pi[t-1] - pi_e[t-1])

        # 3. Ставка ЦБ (делегируем стратегии)
        i_nom[t] = strategy.get_interest_rate(t, pi, x)

        # 4. Реальная ставка
        r_real[t] = (1 + i_nom[t]) / (1 + pi_e[t]) - 1

        # 5. Разрыв выпуска
        x_computed = params['rho_x'] * x[t-1] - params['sigma'] * (r_real[t] - params['r_n'])
        x[t] = min(x_computed, params['x_max'])

        # 6. Потенциальный рост
        y_n[t] = params['y0'] - params['k'] * (pi[t] - params['pi_T'])

        # 7. Темп роста ВВП (YoY) — для потерь
        x_lag4 = x_past[0] if t < 4 else x[t-4]
        y_growth[t] = y_n[t] + (x[t] - x_lag4)
        x_past = np.roll(x_past, -1)
        x_past[-1] = x[t]

        # === УРОВНИ ВВП (точно по формулам Приложения 4, стр. 35) ===
        quarterly_pot = y_n[t] / 4
        potential_gdp[t] = potential_gdp[t-1] * (1 + quarterly_pot)
        actual_gdp[t] = potential_gdp[t] * (1 + x[t])
        balanced_gdp[t] = balanced_gdp[t-1] * (1 + params['y0'] / 4)

        # 8. Потери (только в конце года)
        if t % 4 == 3:
            annual_losses[t] = params['y0'] - y_growth[t]
        cum_losses[t] = cum_losses[t-1] + annual_losses[t]

    return ScenarioResult(
        quarters=np.arange(N),
        inflation=pi * 100,
        actual_gdp=actual_gdp,
        potential_gdp=potential_gdp,
        balanced_gdp=balanced_gdp,
        i_nom=i_nom * 100,
        r_real=r_real * 100,
        annual_losses=annual_losses * 100,
        cum_losses=cum_losses * 100
    )
