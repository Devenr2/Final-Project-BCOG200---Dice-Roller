import pygame
import sys
import random

#Skills Dictionary
#These are the different skills of Dungeons and Dragons fifth edition. 
dnd_skills = [
    "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception",
    "History", "Insight", "Intimidation", "Investigation", "Medicine",
    "Nature", "Perception", "Performance", "Persuasion", "Religion",
    "Sleight of Hand", "Stealth", "Survival"
]
# Constants
#Just for setting up the window
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("D&D Dice Roller")
font = pygame.font.SysFont(None, FONT_SIZE)

# Helper functions
def draw_text(text, position, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

#function to display error messages for 2 seconds
#You can change the time.wait number to change how long the error message remains on screen. Every 1000 is another second. 
def display_error(message):
    draw_text(message, (50, HEIGHT // 2), (255, 0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)

#setup the input box for player stats
def input_box(prompt):
    user_input = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        screen.fill(WHITE)
        draw_text(prompt + " " + user_input, (50, 50))
        pygame.display.flip()

    return user_input

#Creating the buttons used for both selecting proficiencies and also selecting skill to roll
def create_proficiency_buttons():
    proficiency_buttons = []
    button_font = pygame.font.SysFont(None, 20)
    proficiency_y = 150
    for skill in dnd_skills:
        proficiency_text = button_font.render(skill, True, BLACK)
        proficiency_rect = proficiency_text.get_rect(topleft=(50, proficiency_y))
        proficiency_button = (proficiency_text, proficiency_rect, False)  # Proficiency button tuple: (text surface, rect, proficiency)
        proficiency_buttons.append(proficiency_button)
        proficiency_y += 30
    return proficiency_buttons

#the actusal error message display system
def error_message(message):
    error_font = pygame.font.SysFont(None, 20)
    error_surface = error_font.render(str(message), True, (255, 0, 0))
    screen.blit(error_surface, (50, 150))  # Adjust the position as needed
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the error message for 2 seconds, again, you can change this

#How we input character stats
def input_character_info():
    name = input_box("Enter character's name:")
    class_ = input_box("Enter character's class:")
    
    # Level Input
    level = get_positive_integer("Enter character's level.:")

    # Skill Proficiency Selection
    proficiency_buttons = create_proficiency_buttons()
    selected_proficiencies = set()
    selecting_proficiencies = True
    while selecting_proficiencies:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in proficiency_buttons:
                    if button[1].collidepoint(event.pos):
                        button_index = proficiency_buttons.index(button)
                        selected_proficiency = dnd_skills[button_index]
                        if button[2]:
                            selected_proficiencies.remove(selected_proficiency)
                        else:
                            selected_proficiencies.add(selected_proficiency)
                        button = button[0], button[1], not button[2]
                        proficiency_buttons[button_index] = button
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selecting_proficiencies = False
        #don't forget to always add the screen.fill(white) when wanting something to show up here and not just in the terminal
        screen.fill(WHITE)
        draw_text("Select skill proficiencies (Press Enter to proceed):", (50, 100))
        for button in proficiency_buttons:
            color = (0, 255, 0) if button[2] else (255, 0, 0)
            pygame.draw.rect(screen, color, button[1], 2)
            screen.blit(button[0], button[1].topleft)
        pygame.display.flip()

    # Stat Inputs with Error Handling
    # ALL DND stats are whole numbers 1-20 (at least for normal characters. This program does not handle gods well)
    stats = {}
    stat_names = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    for stat_name in stat_names:
        while True:
            stat_str = input_box(f"Enter {stat_name}:")
            try:
                stat_value = int(stat_str)
                if not (1 <= stat_value <= 20):
                    raise ValueError("Stat value must be between 1 and 20.")
                stats[stat_name] = stat_value
                break
            except ValueError as e:
                error_message(e)

    return name, class_, level, selected_proficiencies, stats

#This funcion handles the error message for if a user trys to use a number not between 1 and 20
def get_positive_integer(prompt):
    while True:
        level_str = input_box(prompt)
        try:
            level = int(level_str)
            if 1 <= level <= 20:
                return level
            else:
                raise ValueError("Level must be between 1 and 20.")
        except ValueError as e:
            display_error(e)


#This might seem redundant to have, but it lets me draw on just the Get_Stats part by name without having to rerun the whole character creator
def get_stat_input(stat_name):
    while True:
        stat_str = input_box(f"Enter {stat_name}:")
        try:
            stat_value = int(stat_str)
            if not (1 <= stat_value <= 20):
                raise ValueError("Stat value must be between 1 and 20.")
            return stat_value
        except ValueError as e:
            display_error(e)

#Again, the skill buttons
def create_skill_buttons():
    skill_buttons = []
    button_font = pygame.font.SysFont(None, 20)
    skill_y = 150
    for skill in dnd_skills:
        skill_text = button_font.render(skill, True, BLACK)
        skill_rect = skill_text.get_rect(topleft=(50, skill_y))
        skill_button = (skill_text, skill_rect, False)  # Skill button tuple: (text surface, rect, proficiency)
        skill_buttons.append(skill_button)
        skill_y += 30
    return skill_buttons

#Whole bunch of buttons to show the skill proficiencies you can have
#Red is not proficient, green means proficient
def skill_selection_screen():
    skill_buttons = create_skill_buttons()
    selected_skill = None
    while not selected_skill:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in skill_buttons:
                    if button[1].collidepoint(event.pos):
                        button_index = skill_buttons.index(button)
                        selected_skill = dnd_skills[button_index]
                        break

        screen.fill(WHITE)
        draw_text("Select Skill to Roll:", (50, 100))
        for button in skill_buttons:
            color = (0, 255, 0) if button[2] else (255, 0, 0)
            pygame.draw.rect(screen, color, button[1], 2)
            screen.blit(button[0], button[1].topleft)
        pygame.display.flip()

    return selected_skill

def draw_skills():
    skill_font = pygame.font.SysFont(None, 24)
    skill_y = 150
    for skill in dnd_skills:
        skill_text = skill_font.render(skill, True, BLACK)
        screen.blit(skill_text, (50, skill_y))
        skill_y += 30

def get_stat_modifier(skill, stats):
    # Define which stat corresponds to each skill via a dictionary like earlier
    #Each and every skill in DND is related to a Stat. This dictionary lets me define that relationship and thus allows you to add stat based modifiers to skill based dice rolls
    skill_to_stat = {
        "Acrobatics": "Dexterity",
        "Animal Handling": "Wisdom",
        "Arcana": "Intelligence",
        "Athletics": "Strength",
        "Deception": "Charisma",
        "History": "Intelligence",
        "Insight": "Wisdom",
        "Intimidation": "Charisma",
        "Investigation": "Intelligence",
        "Medicine": "Wisdom",
        "Nature": "Intelligence",
        "Perception": "Wisdom",
        "Performance": "Charisma",
        "Persuasion": "Charisma",
        "Religion": "Intelligence",
        "Sleight of Hand": "Dexterity",
        "Stealth": "Dexterity",
        "Survival": "Wisdom"
    }
    # Get the associated stat for the skill
    stat = skill_to_stat.get(skill)
    if stat:
        # Calculate the modifier based on the character's stats
        #DND stats are taken by taking the raw stat number, subtracting 10, then deviding by two and rounding
        #YES, THEY CAN BE NEGATIVE
        stat_value = stats.get(stat, 10) 
        modifier = (stat_value - 10) // 2
        return modifier
    else:
        return 0  # Return 0 if no associated stat found, just in case. The error message system should prevent this though


def roll_dice(level, selected_proficiencies, selected_skill, stats, roll_type):
    # Roll dice based on the roll type
    #Advantage is rolling 2 twenty sided dice and taking the higher one
    #Disadvantage is rolling 2 twenty sided dice and taking the lower one
    if roll_type == "advantage":
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        roll = max(roll1, roll2) #take the better of the 2 rolls
    elif roll_type == "disadvantage":
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        roll = min(roll1, roll2) #take the worse of the 2 rolls
    else:
        roll = random.randint(1, 20) #flat rolls

    # Calculate proficiency bonus
    #Proficincy bonus in DND is tied directly to character level is ONLY added to rolls if the skill you are rolling is one you are proficient in. 
    if level >= 1 and level <= 4:
        proficiency_bonus = 2
    elif level >= 5 and level <= 8:
        proficiency_bonus = 3
    elif level >= 9 and level <= 12:
        proficiency_bonus = 4
    elif level >= 13 and level <= 16:
        proficiency_bonus = 5
    elif level >= 17 and level <= 20:
        proficiency_bonus = 6
    else:
        proficiency_bonus = 0
    if selected_skill not in selected_proficiencies:
        proficiency_bonus = 0

    # Calculate stat modifier, just use the earlier function
    stat_modifier = get_stat_modifier(selected_skill, stats)

    # Calculate result
    #WOO! MATH
    result = roll + proficiency_bonus + stat_modifier
    
    # Check for critical hits or misses
    #Critical Hits always work, and Critical Misses always fail
    if roll == 20:
        return "natural_20"
    elif roll == 1:
        return "natural_1"
    else:
        return result

# Main function
# Time to put it all together
def main():
    name, class_, level, selected_proficiencies, stats = input_character_info()
    print("Character information:")
    print("Name:", name)
    print("Class:", class_)
    print("Level:", level)
    print("Selected Proficiencies:", selected_proficiencies)
    print("Stats:", stats)

    rolling = False
    skill = None
    roll_type = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not name:
                    name, class_, level, selected_proficiencies, stats = input_character_info()
                elif not skill:
                    skill = skill_selection_screen()
                elif not roll_type:
                    if event.key == pygame.K_a:
                        roll_type = "advantage"
                    elif event.key == pygame.K_d:
                        roll_type = "disadvantage"
                    elif event.key == pygame.K_n:
                        roll_type = "normal"
                elif event.key == pygame.K_SPACE:
                    rolling = True
                    result = roll_dice(level, selected_proficiencies, skill, stats, roll_type)
                    print("You rolled a", result, "for", skill)
                    draw_dice_result_text(result, skill)
                    rolling = False
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    skill = None
                    roll_type = None
                elif event.key == pygame.K_r:
                    skill = None
                    roll_type = None

        screen.fill(WHITE)
        if not rolling:
            draw_character_info(name, class_, level, skill)
            if not roll_type:
                draw_text("Select roll type: (A) Advantage, (D) Disadvantage, (N) Normal", (50, 200))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def draw_character_info(name, class_, level, skill):
    text = "Name: {} Class: {} Level: {} Skill selected: {}".format(name, class_, level, skill)
    draw_text(text, (50, 50))

def draw_dice_result_header(name):
    draw_text(name, (50, 50))

def draw_dice_result_text(result, skill):
    screen.fill(WHITE)
    if result == "natural_20":
        text = "Critical hit! You rolled a natural 20 for {}!".format(skill)
    elif result == "natural_1":
        text = "Critical fail! You rolled a natural 1 for {}!".format(skill)
    elif result > 20:
        text = "NICE! You rolled a {} for {}!".format(result, skill)
    elif result < 1:
        text = "OH NO! You rolled a {} for {}!".format(result, skill)
    else:
        text = "You rolled a {} for {}!".format(result, skill)
    draw_text(text, (50, 100))

if __name__ == "__main__":
    main()
#Man, pygame is pretty cool. Definatly saving this code for personal use in the future. Might cut down on the number of times I lose a die under the table
