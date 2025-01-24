from BlueStacksAppChecker import BlueStacksAppChecker
from GameBot import GameBot
from BarbarianBot import BarbarianBot
from Cordinates import Coordinates
import time


def main():
    startBot = True
    initialBarbarianLevelStart = 11
    if BlueStacksAppChecker.is_bluestacks_running():
        print("BlueStacks is running.")
        bot = GameBot()
        barbarian_bot = BarbarianBot(bot)
        if bot.connect_device():
            bot.set_resolution(1280, 720)
            if startBot:
                while True:
                    isMarching = barbarian_bot.AreTroopsMarching()
                    isInCombat = barbarian_bot.AreTroopsInCombat()
                    print("Marching: " + str(isMarching))
                    print("Combat: " + str(isInCombat))
                    time.sleep(1)

                    if isMarching == False and isInCombat == False:
                        time.sleep(2)
                        barbarian_bot.ClickSearchButton()
                        time.sleep(1)
                        barbarian_bot.SearchForBarbarians()
                        time.sleep(1)

                        # Handle barbarians not found in the map...
                        isSearchButtonPresent = barbarian_bot.IsSearchButtonPresent()
                        time.sleep(0.5)
                        print("Search button present: " + str(isSearchButtonPresent))
                        if isSearchButtonPresent:
                            if initialBarbarianLevelStart < 18:
                                barbarian_bot.IncreaseBarbarianLevel()
                                initialBarbarianLevelStart += 1
                                print("Barbarians level increased to: " + str(initialBarbarianLevelStart))
                            else:
                                barbarian_bot.DecreaseBarbarianLevel()
                                initialBarbarianLevelStart = 10
                                print("Barbarians level reset to: " + str(initialBarbarianLevelStart))
                            time.sleep(1)
                            barbarian_bot.SearchForBarbarians()

                        if isSearchButtonPresent:
                            time.sleep(2)
                        else:
                            time.sleep(1)
                        barbarian_bot.MarkTheBarbarians()
                        time.sleep(0.5)
                        barbarian_bot.ClickAttackButton()
                        time.sleep(0.5)
                        barbarian_bot.SelectTroops()
                        time.sleep(0.5)
                        barbarian_bot.MarchAndStartAttack()
                        time.sleep(1)
                    while barbarian_bot.AreTroopsMarching():
                        print("Marching to barbarians which will be attacked.")
                        time.sleep(1)
                    print("Marching is done.")
                    time.sleep(2)
                    while barbarian_bot.AreTroopsInCombat():
                        print("In combat.")
                        time.sleep(1)
            else:
                print("Bot will not start!!!")
    else:
        print("BlueStacks is not running. Please start BlueStacks.")


if __name__ == "__main__":
    main()
