from BlueStacksAppChecker import BlueStacksAppChecker
from GameBot import GameBot
from Cordinates import Coordinates
import time


def main():
    startBot = True
    initialBarbarianLevelStart = 11
    if BlueStacksAppChecker.is_bluestacks_running():
        print("BlueStacks is running.")
        bot = GameBot()
        if bot.connect_device():
            bot.set_resolution(1280, 720)
            isSearchButtonPresent = bot.isSearchButtonPresent()
            print("Search button present: " + str(isSearchButtonPresent))
            if startBot:
                while True:
                    isMarching = bot.isMarching()
                    isInCombat = bot.isInCombat()
                    print("Marching: " + str(isMarching))
                    print("Combat: " + str(isInCombat))
                    time.sleep(1)

                    if isMarching == False and isInCombat == False:
                        time.sleep(2)
                        bot.click_button(*Coordinates.SEARCH_BAR)  # Click on the search bar
                        time.sleep(1)
                        bot.click_button(*Coordinates.SEARCH_BARBARIANS_BUTTON)  # Click on the search barbarians button
                        time.sleep(1)

                        # Handle barbarians not found in the map...
                        isSearchButtonPresent = bot.isSearchButtonPresent()
                        if isSearchButtonPresent:
                            if initialBarbarianLevelStart < 18:
                                bot.click_button(*Coordinates.INCREASE_BARBARIAN_LEVEL)
                                initialBarbarianLevelStart += 1
                                print("Barbarians level increased to: " + str(initialBarbarianLevelStart))
                            else:
                                bot.click_button(*Coordinates.DECREASE_BARBARIAN_LEVEL)
                                initialBarbarianLevelStart = 10
                                print("Barbarians level reset to: " + str(initialBarbarianLevelStart))
                            time.sleep(1)
                            bot.click_button(*Coordinates.SEARCH_BARBARIANS_BUTTON)  # Click on the search barbarians button

                        if isSearchButtonPresent:
                            time.sleep(2)
                        else:
                            time.sleep(1)
                        bot.click_button(*Coordinates.BARBARIANS)  # Click on barbarians
                        time.sleep(0.5)
                        bot.click_button(*Coordinates.ATTACK_BUTTON)  # Click Attack button
                        time.sleep(0.5)
                        bot.click_button(*Coordinates.SELECT_TROOPS)  # select troops
                        time.sleep(0.5)
                        bot.click_button(*Coordinates.START_ATTACK)  # Start the attack
                        time.sleep(1)
                    while bot.isMarching():
                        print("Marching to troops which will be attacked.")
                        time.sleep(1)
                    print("Marching is done.")
                    time.sleep(2)
                    while bot.isInCombat():
                        print("In combat.")
                        time.sleep(1)
            else:
                print("Bot will not start!!!")
    else:
        print("BlueStacks is not running. Please start BlueStacks.")


if __name__ == "__main__":
    main()
