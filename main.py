from plots import (
    plot_cumulative_losses_comparison_4_results,
    plot_key_rate_comparison,
    plot_losses,
    plot_main_indicators,
)
from policies import (
    build_scenario_1_strategy,
    build_scenario_2_strategy,
    build_scenario_3_strategy,
    build_scenario_4_strategy,
)
from simulation import simulate_scenario

if __name__ == '__main__':
    # Стратегии инкапсулируют параметры и правило расчета ключевой ставки.
    scen1 = simulate_scenario(build_scenario_1_strategy())
    scen2 = simulate_scenario(build_scenario_2_strategy())
    scen3 = simulate_scenario(build_scenario_3_strategy())
    scen4 = simulate_scenario(build_scenario_4_strategy())

    # Основные ряды по статье (инфляция, ВВП, ставки) — по одному окну на сценарий
    plot_main_indicators(scen1, 'Сценарий 1 (ставка 3%)')
    plot_main_indicators(scen2, 'Сценарий 2 (ставка = инфляции)')
    plot_main_indicators(scen3, 'Сценарий 3 (исправление через 1 год)')
    plot_main_indicators(scen4, 'Сценарий 4 (исправление через 3 года)')

    # Годовые и кумулятивные потери темпа роста ВВП (п.п.) по сценариям
    plot_losses(scen1, 'Рис. 3. Потери ВВП в сценарии 1')
    plot_losses(scen2, 'Рис. 5. Потери ВВП в сценарии 2')
    plot_losses(scen3, 'Рис. 7. Потери ВВП в сценарии 3')
    plot_losses(scen4, 'Рис. 9. Потери ВВП в сценарии 4')

    # Сравнение всех сценариев (кумулятив) и динамика ставки для 3 vs 4
    plot_cumulative_losses_comparison_4_results(scen1, scen2, scen3, scen4)
    plot_key_rate_comparison(scen3, scen4)

    print("-------- END --------")
