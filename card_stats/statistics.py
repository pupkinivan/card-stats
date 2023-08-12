from math import comb
from typing import Sequence, Mapping, Union

# import matplotlib.pyplot as plt
import numpy as np

from models import Colors
from util import reduce_sum


def hypergeometric(k: int, n: int, K: int, N: int) -> float:
    """Calculate the probability of getting `k` number of successes in `n`
    number of experiments, with `K` number of items that are considered a
    success in a population of `N`.

    Arguments
        k (int): the number of times a successful element appears in the experiments
        n (int): the total number of experiments
        K (int): the number of elements that would be considered a success
        N (int): the total number of elements, both successful and unsuccessful

    Returns
        proabability (float): the probability of the input scenario
    """
    return comb(K, k) * comb(N - K, n - k) / comb(N, n)


def measure_land_probability_after_draw(
    lands_drawed: int, deck_size: int, total_lands: int, total_past_draws: int
) -> float:
    N = deck_size - total_past_draws
    K = total_lands - lands_drawed
    theta = K / N
    return theta


def high_cost_card_probability(total_high_cost_cards: int, deck_size: int) -> float:
    return total_high_cost_cards / deck_size


def initial_statistics(deck_size: int, hand_size: int, lands: Mapping[Colors, int]):
    total_lands = reduce_sum(lands)
    results = [
        "The probability of drawing 2 {} lands in a {:d}-card hand out of a deck of size {:d} is {:0.4f}".format(
            color.value,
            hand_size,
            deck_size,
            hypergeometric(2, hand_size, color_amounts, deck_size),
        )
        for color, color_amounts in lands.items()
    ]
    results.append(
        "The probability of drawing 3 lands (any color) in a {:d}-card hand out of a deck of size {:d} is {:0.4f}".format(
            hand_size,
            deck_size,
            hypergeometric(3, hand_size, total_lands, deck_size),
        )
    )
    [print(result) for result in results]
    return results


def get_updated_statistics(
    lands_drawn: Mapping[Colors, int],
    deck_size: int,
    draws: int,
    lands: Mapping[Colors, int],
    creatures: int = 0,
):
    k_all = reduce_sum({c: a for c, a in lands_drawn.items() if c != Colors.NONLAND})
    K_all = reduce_sum({c: a for c, a in lands.items() if c != Colors.NONLAND})
    results = {
        "global": "The probability of having drawn {:d} lands in {:d} draws is {:0.4f}".format(
            k_all,
            draws,
            deck_size,
            hypergeometric(k_all, draws, K_all, deck_size),
        )
    }

    remaining_lands = {
        color: lands[color] - lands_drawn[color]
        for color in lands.keys()
        if color != Colors.NONLAND
    }
    remaining_deck = deck_size - draws

    for color in lands:
        results[color.value] = {
            "observed": "The probability of {} {} in {} draws with {}/{} total {} lands is {:0.4f}".format(
                lands_drawn[color],
                color.value,
                draws,
                lands[color],
                deck_size,
                color,
                hypergeometric(lands_drawn[color], draws, lands[color], deck_size),
            ),
            "next": "The probability of drawing a {} next is {:0.4f}".format(
                color.value,
                measure_land_probability_after_draw(
                    lands_drawn[color], deck_size, lands[color], draws
                ),
            ),
        }
    return results


def play_initialized(
    lands_drawn: Mapping[Colors, int],
    deck_size: int,
    hand_size: int,
    lands: Mapping[Colors, int],
    creatures: int = 0,
):
    k_both = reduce_sum(lands_drawn)
    K_both = reduce_sum(lands)
    results = {
        "global": "The probability of having drawn {:d} lands in a {:d}-card hand out of a deck of size {:d} is {:0.4f}".format(
            k_both,
            hand_size,
            deck_size,
            hypergeometric(k_both, hand_size, K_both, deck_size),
        )
    }

    remaining_lands = {
        color: original - drawn for (color, original), drawn in zip(lands, lands_drawn)
    }
    remaining_deck = deck_size - hand_size

    for color in lands:
        color_name = color.value
        results[color.value] = {
            "observed": "The probability of {} {} lands in {} draws with {}/{} total {} lands is {:0.4f}".format(
                lands_drawn[color_name],
                color_name,
                hand_size,
                lands[color_name],
                deck_size,
                color_name,
                hypergeometric(
                    lands_drawn[color_name], hand_size, lands[color.value], deck_size
                ),
            ),
            "next": "The probability of drawing a {} land next is {:0.4f}".format(
                color_name,
                measure_land_probability_after_draw(
                    lands_drawn[color_name], deck_size, lands[color_name], hand_size
                ),
            ),
        }
    for i in range(1):
        yield results
    # return results

    # TODO complete
    while True:
        remaining_deck -= 1
        hand_size += 1
        last_card_drawed = input("-------- Card drawed: ")
        print("Last card drawed: {}".format(last_card_drawed))
        if (answer := input(f"Drawed a land [y/n]?: ")) == "y":
            is_first_color_land = (
                True
                if (answer := input(f"Is it {first_color} or {second_color}?: "))
                == first_color
                else False
            )
            if is_first_color_land:
                k_first_color += 1
                remaining_first_color -= 1
            else:
                k_second_color += 1
                remaining_second_color -= 1

        first_color_probability = measure_land_probability_after_draw(
            k_first_color, deck_size, K_first_color, hand_size
        )
        second_color_probability = measure_land_probability_after_draw(
            k_second_color, deck_size, K_second_color, hand_size
        )
        print(
            "The probability of drawing a {} land next is {:0.4f}".format(
                first_color,
                first_color_probability,
            )
        )
        print(
            "The probability of drawing a {} land next is {:0.4f}".format(
                second_color,
                second_color_probability,
            )
        )


def play():
    first_color: str = input("First color: ")
    second_color = input("Second color: ")
    K_first_color = (
        int(answer)
        if (answer := input(f"Number of {first_color} lands in the population [10]: "))
        is not None
        else 10
    )
    K_second_color = (
        int(answer)
        if (answer := input(f"Number of {second_color} lands in the population [10]: "))
        is not None
        else 10
    )
    k_first_color = (
        int(answer)
        if (answer := input(f"Number of {first_color} lands drawed [0]: ")) != ""
        else 0
    )
    k_second_color = (
        int(answer)
        if (answer := input(f"Number of {second_color} lands drawed [0]: ")) != ""
        else 0
    )
    n = int(answer) if (answer := input("Number of draws [7]: ")) != "" else 7
    N = int(answer) if (answer := input("Size of the deck [60]: ")) != "" else 60
    print(
        "The probability of drawing a land having 3 lands in a {:d}-card hand out of a deck of size {:d} is {:0.4f}".format(
            n, N, hypergeometric(3, 7, 22, deck_size)
        )
    )

    remaining_first_color = K_first_color - k_first_color
    remaining_second_color = K_second_color - k_second_color
    remaining_deck = N - n

    print(
        "The probability of {} {} lands in {} draws with {}/{} total {} lands is {:0.4f}".format(
            k_first_color,
            first_color,
            n,
            K_first_color,
            N,
            first_color,
            hypergeometric(k_first_color, n, K_first_color, N),
        )
    )

    print(
        "The probability of {} {} lands in {} draws with {}/{} total {} lands is {:0.4f}".format(
            k_second_color,
            second_color,
            n,
            K_second_color,
            N,
            second_color,
            hypergeometric(k_second_color, n, K_second_color, N),
        )
    )

    print(
        "The probability of drawing a {} land next is {:0.4f}".format(
            first_color,
            measure_land_probability_after_draw(k_first_color, N, K_first_color, n),
        )
    )

    print(
        "The probability of drawing a {} land next is {:0.4f}".format(
            second_color,
            measure_land_probability_after_draw(k_first_color, N, K_first_color, n),
        )
    )

    while True:
        remaining_deck -= 1
        n += 1
        last_card_drawed = input("-------- Card drawed: ")
        print("Last card drawed: {}".format(last_card_drawed))
        if (answer := input(f"Drawed a land [y/n]?: ")) == "y":
            is_first_color_land = (
                True
                if (answer := input(f"Is it {first_color} or {second_color}?: "))
                == first_color
                else False
            )
            if is_first_color_land:
                k_first_color += 1
                remaining_first_color -= 1
            else:
                k_second_color += 1
                remaining_second_color -= 1

        first_color_probability = measure_land_probability_after_draw(
            k_first_color, N, K_first_color, n
        )
        second_color_probability = measure_land_probability_after_draw(
            k_second_color, N, K_second_color, n
        )
        print(
            "The probability of drawing a {} land next is {:0.4f}".format(
                first_color,
                first_color_probability,
            )
        )
        print(
            "The probability of drawing a {} land next is {:0.4f}".format(
                second_color,
                second_color_probability,
            )
        )


def design_deck(deck_size: int, first_draw: int, desired_energy: int):
    x_space = list(range(1, deck_size + 1))
    probability_of_x = []
    for x in x_space:
        probability_of_x.append(
            hypergeometric(desired_energy, first_draw, x, deck_size)
        )
    optimal_number_of_energies = np.argmax(probability_of_x) + 1
    # fig = plt.figure(figsize=(18, 8))
    # ax = plt.axes()
    # ax.plot(x_space, probability_of_x)
    # ax.set_title("Optimal number of energies: {}".format(optimal_number_of_energies))
    # fig.show()
    return x_space, probability_of_x, optimal_number_of_energies


if __name__ == "__main__":
    # play()
    deck_size = 40
    desired_lands = 3
    land_amount, probability_of_two_lands, optimal_lands = design_deck(
        deck_size=deck_size, first_draw=7, desired_energy=desired_lands
    )
    for lands, proba in zip(land_amount, probability_of_two_lands):
        print(
            "{} lands, {:0.4f} probability {}".format(
                lands,
                proba,
                f"<- Max probability for a {deck_size}-card deck, {desired_lands}-land draw"
                if lands == optimal_lands
                else "",
            )
        )
