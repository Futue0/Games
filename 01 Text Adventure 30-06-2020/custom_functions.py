# Prints text to screen like an old game (or typewriter style)
# where the characters appear 1 by 1.
# The text is slowed equally across a total time so shorter texts
# with the same total_time will type slower - i.e. can spend more
# time per character than if the text was longer.
def slow_text(text: str, total_time=1):
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
    
