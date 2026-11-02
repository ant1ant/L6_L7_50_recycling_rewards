import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------- reward_points: validation ----------
def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)

def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)

def test_zero_weight_is_valid():
    assert reward_points("plastic", 0, False) == 0


# ---------- reward_points: minimum / bonus ----------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0

def test_exactly_minimum_weight():
    assert reward_points("paper", 5, False) == 0          # extra == 0

def test_paper_no_bonus():
    assert reward_points("paper", 10, False) == 30         # min 5, extra 5

def test_paper_with_bonus():
    assert reward_points("paper", 10, True) == 36          # min 4, extra 6

def test_plastic_with_bonus():
    assert reward_points("plastic", 10, True) == 48        # min 2, extra 8

def test_metal_bonus_ignored():
    assert reward_points("metal", 5, True) == 36           # min stays 2, extra 3

def test_metal_no_bonus():
    assert reward_points("metal", 10, False) == 96         # min 2, extra 8


# ---------- reward_points: extra > 20 boundary ----------
def test_extra_exactly_20_no_boost():
    assert reward_points("paper", 25, False) == 120        # extra 20, rate 6

def test_extra_21_paper_boost():
    assert reward_points("paper", 26, False) == 210        # extra 21, rate 10

def test_extra_over_20_plastic_boost():
    assert reward_points("plastic", 30, False) == 270      # extra 27, rate 10

def test_extra_exactly_20_metal_no_boost():
    assert reward_points("metal", 22, False) == 240        # extra 20, rate 12

def test_extra_over_20_metal_boost():
    assert reward_points("metal", 30, False) == 504        # extra 28, rate 18


# ---------- collection_accepted ----------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True

def test_hazardous_at_limit():
    assert collection_accepted(5, 1, True) is True

def test_hazardous_over_limit():
    assert collection_accepted(6, 1, True) is False

def test_hazardous_ignores_bag_count():
    assert collection_accepted(4, 10, True) is True

def test_non_hazardous_over_50():
    assert collection_accepted(51, 1, False) is False

def test_non_hazardous_exactly_50():
    assert collection_accepted(50, 3, False) is True

def test_exactly_three_bags():
    assert collection_accepted(20, 3, False) is True

def test_four_bags_rejected():
    assert collection_accepted(20, 4, False) is False


# ---------- slot_status ----------
def test_morning_open_boundary():
    assert slot_status(20, True, False) == "open"          # cutoff 20

def test_morning_late_upper():
    assert slot_status(19, True, False) == "late"

def test_morning_late_lower_boundary():
    assert slot_status(5, True, False) == "late"           # cutoff-15

def test_morning_missed():
    assert slot_status(4, True, False) == "missed"

def test_evening_open_boundary():
    assert slot_status(10, False, False) == "open"         # cutoff 10

def test_evening_late_boundary():
    assert slot_status(-5, False, False) == "late"

def test_evening_missed():
    assert slot_status(-6, False, False) == "missed"

def test_holiday_morning_open():
    assert slot_status(35, True, True) == "open"           # cutoff 35

def test_holiday_morning_late():
    assert slot_status(20, True, True) == "late"

def test_holiday_morning_missed():
    assert slot_status(19, True, True) == "missed"

def test_holiday_evening_open():
    assert slot_status(25, False, True) == "open"          # cutoff 25

def test_holiday_evening_missed():
    assert slot_status(9, False, True) == "missed"
