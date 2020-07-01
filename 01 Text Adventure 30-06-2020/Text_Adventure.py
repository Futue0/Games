# Robin Vize 30-06-2020.
# Basic text adventure, fantasy game.
# Run from Python IDLE otherwise the delays don't work with Windows cmd.

from custom_functions import *
from time import sleep

loop = True

while loop:
    # Story introduction for the player.
    # Premise and some flavour.
    slow_text("In the beginning there was a tiny elf.")
    slow_text("This little cutey was called Squab.")
    sleep(1)
    slow_text("He was very...", 1)
    sleep(1)
    slow_text("EVIL!!!", 3)
    print("")

    # Player introduction and setup.
    slow_text("Bartender: Hello traveller. How can I help you?")
    slow_text("The Inn offers food and drink, a place to stay or a friendly chat.")

    response_accepted = False
    food_drink_keywords = ("food", "eat", "drink", "beer", "wine")
    sleep_room_keywords = ("tired", "sleep", "room", "stay", "bed")
    chat_keywords = ("chat", "talk", "listen")

    # Get the players answer.
    while not response_accepted:
        response = input("You: ").lower()
        
        for word in food_drink_keywords:
            if word in response:
                response_chosen = "FOOD"
                response_accepted = True
                
        for word in sleep_room_keywords:
            if word in response:
                response_chosen = "SLEEP"
                response_accepted = True
            
        for word in chat_keywords:
            if word in response:
                response_chosen = "CHAT"
                response_accepted = True

        if not response_accepted:        
            slow_text("Bartender: Sorry, can you rephrase that?", 1)

    # Bartender responses.
    if response_chosen == "FOOD":
        food_response()
    elif response_chosen == "SLEEP":
        sleep_response()
    else:
        chat_response()

    # Get players name.
    class Player:

        def __init__(self, name):
            self.name = name

    player_name = input("You: My name is ")

    player = Player(player_name)

    # Conflict appears.
    slow_text("You've only just spoken your name when you hear a bang behind you.")
    slow_text("Turning around you see a cute, little elf standing in the entrance.")
    slow_text("Elf: Well, well, well, well. Of course you're here {}.".format(player.name))
    slow_text("Elf: This is the part where I introduce myself before I kill you. It's Squab.")
    slow_text("Squab: Meet you end {}!".format(player.name.upper()))
    slow_text("The elf charges at you with a very large spoon (or maybe he's just far away?)")
    slow_text("Do you want to fight or ignore him?")

    # Player against Squab.
    response_accepted = False

    while not response_accepted:
        response = input("You... ").lower()

        if "fight" or "attack" or "stab" or "kill" in response:
            second_response_chosen = "FIGHT"
            response_accepted = True
        elif "ignore" or "dodge" or "avoid" or "nothing" in response:
            second_response_chosen = "IGNORE"
            response_accetped = True

        if not response_accepted:
            slow_text('Try entering "fight" or "ignore".')

    # Win or lose?
    if second_response_chosen == "FIGHT":
        fight_squab(response_chosen)
    else:
        ignore_squab()

    # Try again or exit?
    response = input('Type "quit" to exit or anything/enter to try again.')
    if response.lower() == "quit":
        loop = False
