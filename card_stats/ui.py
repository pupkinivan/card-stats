from functools import partial

import streamlit as st

from main import initial_statistics, play_initialized, get_updated_statistics
from models import Colors
from util import reduce_sum


def get_initial_stats():
    initial_stats = initial_statistics(
        st.session_state.deck_size,
        st.session_state.hand_size,
        {Colors.of(c): a for c, a in zip(color_names, color_amounts)},
    )
    text = "\n".join(initial_stats)
    st.session_state.stats = text


st.title("Card game")

if "deck_size" not in st.session_state:
    st.session_state["deck_size"] = st.number_input(
        "Deck size",
        min_value=40,
        max_value=100,
        value=60,
        step=1,
    )

if "hand_size" not in st.session_state:
    st.session_state["hand_size"] = st.number_input(
        "Initial draw size", min_value=1, max_value=10, value=7
    )

number_of_colors = st.number_input(
    "Number of different land colors",
    min_value=1,
    max_value=6,
    value=1,
    step=1,
)

color_names = []
color_amounts = []
for i in range(number_of_colors):
    color_names.append(st.text_input(f"Color name {i+1}", placeholder="Color name"))
    color_amounts.append(
        st.number_input(f"Amount of {color_names[i]} lands ", value=12, step=1)
    )
deck_lands = {Colors.of(c): a for c, a in zip(color_names, color_amounts)}
deck_lands[Colors.NONLAND] = st.session_state.deck_size - reduce_sum(deck_lands)

if "stats_text" not in st.session_state:
    st.session_state.stats = ""
st.session_state["stats_text"] = st.text_area(
    label="Statistics",
    value=st.session_state.stats,
)
initial_stats = st.button("Compute initial stats", on_click=get_initial_stats)

if "drawn" not in st.session_state:
    drawn = {Colors.of(c): 0 for c in color_names}
    drawn[Colors.NONLAND] = 0
    st.session_state["drawn"] = drawn


def update_stats(color: Colors):
    st.session_state.drawn[color] = int(st.session_state.drawn[color]) + 1
    results = get_updated_statistics(
        st.session_state.drawn,
        st.session_state.deck_size,
        draws=reduce_sum(st.session_state.drawn),
        lands=deck_lands,
    )
    result = []
    for color in st.session_state.drawn.keys():
        for result_type in ["observed", "next"]:
            result.append(results[color.value][result_type])
    st.session_state.stats = "\n".join(result)


draw_card = {
    Colors.of(color_name): partial(update_stats, Colors.of(color_name))
    for color_name in color_names
}
draw_card[Colors.NONLAND] = partial(update_stats, Colors.NONLAND)

for color_name in color_names:
    color = Colors.of(color_name)
    st.text(f"Drawn {st.session_state.drawn[color]} {color.value} lands")
    st.button(f"Drawed a {color.value} land (+1)", on_click=draw_card[color])
st.text(f"Drawn {st.session_state.drawn[Colors.NONLAND]} {Colors.NONLAND.value} lands")
st.button("Drawed a nonland", on_click=draw_card[Colors.NONLAND])

# def start_game_callback(colors, deck_size, hand_size):
#     def start_turns():
#         for turn in play_initialized(drawn_lands, deck_size, hand_size, colors):
#             st.text_area("Turn outputs", value=turn)

#     def stop_game():
#         exit(0)

#     drawn_lands = {
#         st.number_input(
#             f"Drawn {color.value} lands", min_value=0, max_value=100, value=0
#         )
#         for color in colors.keys()
#     }
#     st.button("Start turns", on_click=start_turns)
#     st.button("Finish game", on_click=stop_game)


# start_game = partial(
#     start_game_callback,
#     {Colors.of(c): a for c, a in zip(color_names, color_amounts)},
#     deck_size,
#     hand_size,
# )
# st.button("Start game", on_click=start_game)
