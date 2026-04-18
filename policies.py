from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np
import numpy.typing as npt

from params import params


class InterestRateStrategy(Protocol):
    """Контракт стратегии: вернуть номинальную ставку (в долях) на шаге t."""

    def get_interest_rate(
        self,
        t: int,
        pi: npt.NDArray[np.float64],
        x: npt.NDArray[np.float64],
    ) -> float:
        """Вычисляет номинальную ставку i_nom[t]."""


@dataclass(frozen=True)
class ConstantRateStrategy:
    """Фиксированная ставка в фазе ошибки."""

    rate: float = 0.03

    def get_interest_rate(
        self,
        t: int,
        pi: npt.NDArray[np.float64],
        x: npt.NDArray[np.float64],
    ) -> float:
        return self.rate


@dataclass(frozen=True)
class InflationIndexedStrategy:
    """Ставка равна текущей инфляции pi[t]."""

    def get_interest_rate(
        self,
        t: int,
        pi: npt.NDArray[np.float64],
        x: npt.NDArray[np.float64],
    ) -> float:
        return float(pi[t])


@dataclass(frozen=True)
class TaylorRuleStrategy:
    """Правило Тейлора на лагах x[t-1], pi[t-1] с параметрами из params."""

    i_n: float = params["i_n"]
    phi_x: float = params["phi_x"]
    phi_pi: float = params["phi_pi"]
    pi_target: float = params["pi_T"]

    def get_interest_rate(
        self,
        t: int,
        pi: npt.NDArray[np.float64],
        x: npt.NDArray[np.float64],
    ) -> float:
        return self.i_n + self.phi_x * x[t - 1] + self.phi_pi * (pi[t - 1] - self.pi_target)


@dataclass(frozen=True)
class ErrorThenTaylorStrategy:
    """
    До correction_quarters использует error_strategy, затем переключается на Taylor.

    Если correction_quarters == 0, переключение не происходит (вечная фаза ошибки).
    """

    error_strategy: InterestRateStrategy
    correction_quarters: int = 0
    taylor_strategy: InterestRateStrategy = TaylorRuleStrategy()

    def get_interest_rate(
        self,
        t: int,
        pi: npt.NDArray[np.float64],
        x: npt.NDArray[np.float64],
    ) -> float:
        in_error = (self.correction_quarters == 0) or (t < self.correction_quarters)
        if in_error:
            return self.error_strategy.get_interest_rate(t, pi, x)
        return self.taylor_strategy.get_interest_rate(t, pi, x)


def build_scenario_1_strategy() -> InterestRateStrategy:
    """Сценарий 1: ставка 3% на всем горизонте."""
    return ErrorThenTaylorStrategy(error_strategy=ConstantRateStrategy(rate=0.03), correction_quarters=0)


def build_scenario_2_strategy() -> InterestRateStrategy:
    """Сценарий 2: ставка равна инфляции на всем горизонте."""
    return ErrorThenTaylorStrategy(error_strategy=InflationIndexedStrategy(), correction_quarters=0)


def build_scenario_3_strategy() -> InterestRateStrategy:
    """Сценарий 3: 1 год ошибки (4 квартала), затем правило Тейлора."""
    return ErrorThenTaylorStrategy(error_strategy=InflationIndexedStrategy(), correction_quarters=4)


def build_scenario_4_strategy() -> InterestRateStrategy:
    """Сценарий 4: 3 года ошибки (12 кварталов), затем правило Тейлора."""
    return ErrorThenTaylorStrategy(error_strategy=InflationIndexedStrategy(), correction_quarters=12)
