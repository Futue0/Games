# Prints text to screen like an old game (or typewriter style)
# where the characters appear 1 by 1.
# The text is slowed equally across a total time so shorter texts
# with the same total_time will type slower - i.e. can spend more
# time per character than if the text was longer.
def slow_text(text: str, total_time=2):
    from time import sleep
    from sys import exc_info

    try:
        # type check to catch if text is string
        # note that len() also works for list objects
        # so this isn't fool proof (but does raise on int/float)
        text_length = len(text)
        sleep_per_character = total_time / text_length
        
        for each_character in text:
            print(each_character, end='')
            sleep(sleep_per_character)

        print("")
    except:
        print("Unexpected error:", exc_info()[0])
        raise

# Bartender response on player asking for food/drink.
def food_response():
    slow_text("Bartender: Okay, here's a plate of house special and glass of it too.")
    slow_text("The bartender slides a plate and glass over. They certainly are special.")
    slow_text("Bartender: What name am I putting on the tab?")

# Bartender response on player asking to sleep/for a room.
def sleep_response():
    slow_text("Bartender: Single rooms are 1g per night. Seems appropriate seeing as you're alone.")
    slow_text("The bartender places a rusty key on the bar and tells you it's the room at the end.")
    slow_text("Bartender: What name are you booking in under?")

# Bartender response on player asking to chat.
def chat_response():
    slow_text("Bartender: Praise Jesus, I haven't had a single customer all year and I'm lonely.")
    slow_text("The bartender wipes a single tear from his eye. What a loser.")
    slow_text("Bartender: Let's start with names shall we? Mine is Frimtickles.")

# Fight Squab.
def fight_squab(weapon):
    if weapon == "FOOD":
        weapon = "knife"
        slow_text("Good luck that you have food. Even better luck that it was served with a knife and fork.")
    elif weapon == "SLEEP":
        weapon = "key"
        slow_text("A room key versus a spoon? What sort of fight is this? Honestly...")
    else:
        slow_text("It's a shame you don't have anything to defend yourself with at hand.")
        slow_text("Squab overpowers you with the spoon and takes both your eyes out their sockets.")
        slow_text("It's probably for the best really. You don't want to see what he does next.")
        slow_text("I hope you had life insurance because you're very much dead :(")
        return
        
    slow_text("You steady yourself against the incoming attack.")
    slow_text("This elf reminds you of a child, albeit a very angry one.")
    slow_text("It's not much of a fight. Think you're a big man? Killing a child?")
    slow_text("Regretfully you brandish your weapon, plunging your {} into the elf.".format(weapon))
    slow_text("Yup, that will do it. He's dead, Mr Brave. I hope you're proud of yourself.")

# Ignore Squab.
def ignore_squab():
    slow_text("You decide to ignore the person threatening to kill you.")
    slow_text("This doesn't sound like a very good idea in my opinion.")
    slow_text("You turn back around to face the bartender.")
    slow_text("There's a sharp pain in your back. You look down to see the end of a spoon protruding from your lower abdomen")
    slow_text("Told you it was a stupid idea.")
    slow_text("It takes you only 4 seconds to collapse and a further 9 to leave this world entirely")
    
