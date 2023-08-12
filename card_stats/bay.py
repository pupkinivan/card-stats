from typing import Sequence

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm

from models import Colors


def compute_initial_statistics(
    deck_size: int, number_of_lands_per_color: Sequence[int]
):
    with pm.Model() as model_prior:
        # number_of_mana = pm.HyperGeometric("number_of_mana")

        # is_mana_single_distributions = [
        #     pm.Bernoulli(f"is_{color_name}", p=theta)
        #     for color_name, theta in zip(mana_color_names, thetas)
        # ]
        is_mana_single = [
            pm.HyperGeometric(f"is_mana_{color.value}", N=deck_size, k=l, n=7)
            for color, l in zip(mana_color_names, number_of_lands_per_color)
        ]
        is_mana_all = pm.Deterministic(
            "is_mana_all", is_mana_single[0] + is_mana_single[1]
        )
        inference_data = pm.sample()
        # inference_data = pm.sample_prior_predictive(samples=50)
    return inference_data


def update_on_turn(is_mana: bool, color: Colors):
    with pm.Model() as model_ingame:
        is_mana_single = [
            pm.HyperGeometric(f"is_mana_{color}", N=deck_size, k=l, n=7)
            for color, l in zip(mana_color_names, number_of_lands_per_color)
        ]
        is_mana_all = pm.Deterministic(
            "is_mana_all", is_mana_single[0] + is_mana_single[1]
        )
        inference_data = pm.sample()
    return inference_data


# Start game

mana_color_names = [Colors.BLACK, Colors.RED]
number_of_lands_per_color = [12, 10]
deck_size = 65
thetas = [l / deck_size for l in number_of_lands_per_color]

inference_data = compute_initial_statistics(
    deck_size=deck_size, number_of_lands_per_color=number_of_lands_per_color
)

print(inference_data)
# print(inference_data.sample_stats)
# print(inference_data.posterior)

print(az.summary(inference_data, round_to=2))

# Plot prior predictive check
# plt.plot(
#     np.linspace(0, 7, num=8),
#     inference_data.prior["is_mana_all"].stack(sample=("chain", "draw")),
# )
# plt.show()

# Plot posterior
# az.plot_trace(
#     inference_data,
# )  # combined=True
# plt.show()

while True:
    is_finished = input(
        "Drawed a mana? Input color, press enter if it isn't a land, or Ctrl+C for finishing: "
    )
    if is_finished == "exit":
        break
    elif is_finished == "":
        continue
    else:
        color = Colors.of(is_finished.lower())

    update_on_turn()
