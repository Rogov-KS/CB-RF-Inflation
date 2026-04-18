from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from simulation import ScenarioResult


def plot_main_indicators(scen: ScenarioResult, title: str) -> None:
    """
    Четыре панели: инфляция, уровни ВВП, номинальная и реальная ставки (ось X — кварталы).
    Показывает интерактивное окно matplotlib.
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    q = scen['quarters']

    axs[0, 0].plot(q, scen['inflation'], 'b-')
    axs[0, 0].set_title('Инфляция, %')
    axs[0, 0].grid(True)

    # ВВП и потенциальный ВВП — УРОВНИ (индекс 100)
    axs[0, 1].plot(q, scen['balanced_gdp'], 'gray', linestyle='dotted', label='Траектория сбалансированного роста')
    axs[0, 1].plot(q, scen['actual_gdp'], 'k-', label='ВВП')
    axs[0, 1].plot(q, scen['potential_gdp'], 'r--', label='потенциальный ВВП')
    axs[0, 1].set_title('ВВП и потенциальный ВВП')
    axs[0, 1].set_ylim(95, 115)
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    axs[1, 0].plot(q, scen['i_nom'], 'b-')
    axs[1, 0].set_title('Номинальная ставка, %')
    axs[1, 0].set_xlabel('кварталы')
    axs[1, 0].grid(True)

    axs[1, 1].plot(q, scen['r_real'], 'b-')
    axs[1, 1].set_title('Реальная ставка, %')
    axs[1, 1].set_xlabel('кварталы')
    axs[1, 1].grid(True)

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def plot_losses(scen: ScenarioResult, title: str) -> None:
    """Столбцы годовых потерь и линия кумулятивных потерь по годам (1–7)."""
    years = np.arange(1, 8)
    annual = [scen['annual_losses'][3 + 4 * i] for i in range(7)]
    cum_at = [scen['cum_losses'][3 + 4 * i] for i in range(7)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(years, annual, color='red', label='потери темпов роста ВВП')
    ax.plot(years, cum_at, 'k-', label='кумулятивные потери')
    ax.set_xlabel('годы')
    ax.set_ylabel('процентные пункты')
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
    plt.show()


def plot_cumulative_losses_comparison_4_results(
    scen1: ScenarioResult,
    scen2: ScenarioResult,
    scen3: ScenarioResult,
    scen4: ScenarioResult,
) -> None:
    """Сгруппированные столбцы кумулятивных потерь по четырём сценариям (рис. 10)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    years = np.arange(1, 8)
    ax.bar(years - 0.3, [scen1['cum_losses'][3 + 4 * i] for i in range(7)], width=0.2, label='Сценарий 1', color='blue')
    ax.bar(years - 0.1, [scen2['cum_losses'][3 + 4 * i] for i in range(7)], width=0.2, label='Сценарий 2', color='orange')
    ax.bar(years + 0.1, [scen3['cum_losses'][3 + 4 * i] for i in range(7)], width=0.2, label='Сценарий 3', color='green')
    ax.bar(years + 0.3, [scen4['cum_losses'][3 + 4 * i] for i in range(7)], width=0.2, label='Сценарий 4', color='yellow')
    ax.set_xlabel('годы')
    ax.set_ylabel('процентные пункты')
    ax.set_title('Кумулятивные потери темпов роста ВВП')
    ax.grid(True)
    ax.legend()
    plt.show()


def plot_key_rate_comparison(scen3: ScenarioResult, scen4: ScenarioResult) -> None:
    """Номинальная ключевая ставка по кварталам для сценариев 3 и 4 (рис. 11)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(scen3['quarters'], scen3['i_nom'], 'gray', label='Сценарий 3', lw=2)
    ax.plot(scen4['quarters'], scen4['i_nom'], 'blue', label='Сценарий 4', lw=2)
    ax.set_xlabel('кварталы')
    ax.set_ylabel('% годовых')
    ax.set_title('Динамика ключевой ставки')
    ax.grid(True)
    ax.legend()
    plt.show()


def plot_key_rate_comparison_4_results(
    scen1: ScenarioResult,
    scen2: ScenarioResult,
    scen3: ScenarioResult,
    scen4: ScenarioResult,
) -> None:
    """Сравнение динамики номинальной ключевой ставки по всем 4 сценариям."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(scen1['quarters'], scen1['i_nom'], label='Сценарий 1', lw=2, color='tab:blue')
    ax.plot(scen2['quarters'], scen2['i_nom'], label='Сценарий 2', lw=2, color='tab:orange')
    ax.plot(scen3['quarters'], scen3['i_nom'], label='Сценарий 3', lw=2, color='tab:green')
    ax.plot(scen4['quarters'], scen4['i_nom'], label='Сценарий 4', lw=2, color='tab:red')
    ax.set_xlabel('кварталы')
    ax.set_ylabel('% годовых')
    ax.set_title('Сравнение динамики ключевой ставки (4 сценария)')
    ax.grid(True)
    ax.legend()
    plt.show()
