import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------- reward_points ----------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0

def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)

def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)

def test_paper_with_bonus():
    # min 5 -> 4, extra 6, rate 6
    assert reward_points("paper", 10, True) == 36

def test_plastic_normal_rate():
    # min 3, extra 7, rate 6
    assert reward_points("plastic", 10, False) == 42

def test_metal_normal_rate():
    # min 2, extra 8, rate 12
    assert reward_points("metal", 10, False) == 96

def test_plastic_high_extra():
    # min 3, extra 27, rate 6+4
    assert reward_points("plastic", 30, False) == 270

def test_metal_high_extra():
    # min 2, extra 28, rate 12+4+2
    assert reward_points("metal", 30, False) == 504


# ---------- collection_accepted ----------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True

def test_hazardous_within_limit():
    assert collection_accepted(5, 1, True) is True

def test_too_heavy():
    assert collection_accepted(51, 1, False) is False

def test_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# ---------- slot_status ----------
def test_morning_open():
    assert slot_status(25, True, False) == "open"

def test_evening_late():
    assert slot_status(5, False, False) == "late"

def test_morning_missed():
    assert slot_status(0, True, False) == "missed"

def test_holiday_open():
    assert slot_status(35, True, True) == "open"
