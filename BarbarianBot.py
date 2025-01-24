from Cordinates import Coordinates


class BarbarianBot:
    def __init__(self, bot):
        self.bot = bot

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
