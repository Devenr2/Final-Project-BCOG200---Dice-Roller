import pytest
from diceroller import roll_dice, get_stat_modifier

# Test roll_dice function
def test_roll_dice():
    level = 5
    selected_proficiencies = {"Acrobatics"}
    stats = {"Dexterity": 16}  # Example stats for testing

    # Test regular roll with proficiency bonus and stat modifier
    result = roll_dice(level, selected_proficiencies, "Acrobatics", stats)
    assert 1 <= result <= 26  # Assuming max roll with proficiency and modifier won't exceed 26

    # Test roll without proficiency bonus
    result = roll_dice(level, set(), "Acrobatics", stats)
    assert 1 <= result <= 21  # Assuming max roll without proficiency won't exceed 21

    # Test roll without stat modifier
    stats["Dexterity"] = 10
    result = roll_dice(level, selected_proficiencies, "Acrobatics", stats)
    assert 1 <= result <= 25  # Assuming max roll with proficiency but no modifier won't exceed 25

# Test get_stat_modifier function
def test_get_stat_modifier():
    stats = {"Strength": 18, "Dexterity": 10, "Intelligence": 12}
    
    # Test stat modifier calculation for different stats
    assert get_stat_modifier("Athletics", stats) == 4
    assert get_stat_modifier("Acrobatics", stats) == 0
    assert get_stat_modifier("Arcana", stats) == 1
    assert get_stat_modifier("Perception", stats) == 1
    assert get_stat_modifier("Stealth", stats) == 0
