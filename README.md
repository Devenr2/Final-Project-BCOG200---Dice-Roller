# Final-Project-BCOG200---Dice-Roller
Project Pitch:
This project is for a Dice Rolling program that is intended for use with Dungeons and Dragons character. The program will ideally work in two-three parts: character stats and Dice rolling.
You will input your character's raw stat numbers in the first part, and then roll the dice in the second part, while accounting for the specific stat, die type, and advantage or disadvantage. 
I am leaving room for increased capabilities for things such as random character generation, and proficiency rolls

Functions
  1. A function that allows for the user to input their characters name, class, level and raw stat numbers. Alternitavly, I could make a funcition for "random" character generation
  2. A function that allows the user to select the type of dice they wish to roll, what stat it is rolled on, if they have proficieny, and if it has advantage/disadvantage.
  3. A function that actually rolls the die and then outputs the number to the player, with special messages for natural 20's and natural 1's (probably use Numpy for random rolling, and something else for visual component)

INTRODUCTION TEXT

  WELCOME! This is a virtual dice roller for all of your Dungeons and Dragons Dice needs! This program allows you to roll ability checks, to hit rolls, percentile checks, and even damage dice while allowing for advantage, disadvantage and even status conditions. The way to use it is simple: 
  1. First you are going to need to input your character level, ability scores, and proficiencies. Simply enter those numbers when prompted by the program.
  2. Second, you will asked which dice you will be rolling, simply select the appropriate dice from the options shown
  3. Finally, you will be asked if there are any external conditions. This includes if the check is an ability check, if it is made with advantage, and if you are currently cursed.
  The end result is the program will roll the dice for you and give you a simple digit answer. No more having to do the math yourself, or hunt through your character sheet in order to add up your proficiency, abilty score, and status. The program will 'save' your character stats until closed. Enjoy!
