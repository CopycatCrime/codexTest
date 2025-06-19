import sys
from pathlib import Path
import pytest

# Add repository root to sys.path so that 'utils' can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.jinro import Jinro, Villager, Werewolf


def test_start_night_phase_sets_can_act_only_for_alive_members():
    v1 = Villager()
    v2 = Villager()
    v2.alive = False
    wolf = Werewolf()
    game = Jinro([v1, v2, wolf], max_turns=3)

    game.start_night_phase()

    assert v1.can_act is True
    assert wolf.can_act is True
    # dead member should not be able to act
    assert v2.can_act is False


def test_execute_night_actions_kills_target_and_resets_actor_flag():
    wolf = Werewolf()
    villager = Villager()
    game = Jinro([wolf, villager], max_turns=3)

    game.start_night_phase()
    game.execute_night_actions({wolf: villager})

    assert villager.alive is False
    assert wolf.can_act is False  # end_night called in act


def test_end_night_phase_updates_turn_and_game_over():
    v1 = Villager()
    game = Jinro([v1], max_turns=2)

    assert game.get_turn() == 0

    game.start_night_phase()
    game.end_night_phase()
    assert game.get_turn() == 1
    assert game.is_game_over() is False

    game.start_night_phase()
    game.end_night_phase()
    assert game.get_turn() == 2
    assert game.is_game_over() is True


def test_get_alive_members_returns_only_alive_players():
    wolf = Werewolf()
    villager = Villager()
    game = Jinro([wolf, villager], max_turns=3)

    game.start_night_phase()
    game.execute_night_actions({wolf: villager})

    alive = game.get_alive_members()
    assert alive == [wolf]
