from Cordinates import Coordinates
import time


class BarbarianBot:

    def __init__(self, bot):
        self.bot = bot
        self.initialBarbarianLevelStart = 11

    def run_bot(self):
        while True:
            isMarching = self.AreTroopsMarching()
            isInCombat = self.AreTroopsInCombat()
            print("Marching: " + str(isMarching))
            print("Combat: " + str(isInCombat))
            time.sleep(1)
            if not isMarching and not isInCombat:
                self.AttackBarbarians()
            while self.AreTroopsMarching():
                print("Marching to barbarians which will be attacked.")
                time.sleep(1)
            print("Marching is done.")
            time.sleep(2)
            while self.AreTroopsInCombat():
                print("In combat.")
                time.sleep(1)

    def AttackBarbarians(self):
        self.ClickSearchButton()
        time.sleep(1)
        self.SearchForBarbarians()
        time.sleep(1)

        # Handle barbarians not found on the map
        isSearchButtonPresent = self.IsSearchButtonPresent()
        time.sleep(0.5)
        print("Search button present: " + str(isSearchButtonPresent))
        if isSearchButtonPresent:
            if self.initialBarbarianLevelStart < 18:
                self.IncreaseBarbarianLevel()
                self.initialBarbarianLevelStart += 1
                print("Barbarians level increased to: " + str(self.initialBarbarianLevelStart))
            else:
                self.DecreaseBarbarianLevel()
                self.initialBarbarianLevelStart = 10
                print("Barbarians level reset to: " + str(self.initialBarbarianLevelStart))
            time.sleep(1)
            self.SearchForBarbarians()

        if isSearchButtonPresent:
            time.sleep(2)
        else:
            time.sleep(1)
        self.MarkTheBarbarians()
        time.sleep(0.5)
        self.ClickAttackButton()
        time.sleep(0.5)
        self.SelectTroops()
        time.sleep(0.5)
        self.MarchAndStartAttack()
        time.sleep(1)

    def ClickSearchButton(self):
        self.bot.click_button(*Coordinates.SEARCH_BAR)  # Click on the search bar

    def SearchForBarbarians(self):
        self.bot.click_button(*Coordinates.SEARCH_BARBARIANS_BUTTON)  # Click on the search barbarians button

    def IncreaseBarbarianLevel(self):
        self.bot.click_button(*Coordinates.INCREASE_BARBARIAN_LEVEL)

    def DecreaseBarbarianLevel(self):
        self.bot.click_button(*Coordinates.DECREASE_BARBARIAN_LEVEL)

    def MarkTheBarbarians(self):
        self.bot.click_button(*Coordinates.BARBARIANS)  # Click on barbarians

    def ClickAttackButton(self):
        self.bot.click_button(*Coordinates.ATTACK_BUTTON)  # Click Attack button

    def SelectTroops(self):
        self.bot.click_button(*Coordinates.SELECT_TROOPS)  # select troops

    def MarchAndStartAttack(self):
        self.bot.click_button(*Coordinates.START_ATTACK)  # Start the attack

    def IsSearchButtonPresent(self):
        return self.bot.isSearchButtonPresent()

    def AreTroopsMarching(self):
        return self.bot.isMarching()

    def AreTroopsInCombat(self):
        return self.bot.isInCombat()
