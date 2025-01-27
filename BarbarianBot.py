from Cordinates import Coordinates
from TroopsScanner import TroopsScanner
import time
import glob


class BarbarianBot:
    def __init__(self, emulator):
        self.emulator = emulator
        self.initialBarbarianLevelStart = 11
        self.troopsScanner = TroopsScanner(emulator)
        self.maximumPercentageThatTroopsAreAllowedToDecrease = 1
        self.checkForHealingIntervalMinutes = 10
        self.checkForHealingIntervalSeconds = self.checkForHealingIntervalMinutes * 60
        self.checkForHealingLastExecutionTime = time.time()

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

            # Check if troops are decreased and need refilling
            current_time = time.time()
            if current_time - self.checkForHealingLastExecutionTime >= self.checkForHealingIntervalSeconds:
                needHealing = self.troopsScanner.AreTroopsDecreased(self.maximumPercentageThatTroopsAreAllowedToDecrease)
                if needHealing is True:
                    # TODO: Implement healing troops and refilling new troop group
                    print("Troops are decreased. Healing is needed!!!!!!!!!.")
                self.checkForHealingLastExecutionTime = current_time

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
        time.sleep(0.3)
        self.ClickAttackButton()
        time.sleep(0.5)
        self.SelectTroops()
        time.sleep(0.5)
        self.MarchAndStartAttack()
        time.sleep(1)

    def ClickSearchButton(self):
        self.emulator.click_button(*Coordinates.SEARCH_BAR)  # Click on the search bar

    def SearchForBarbarians(self):
        self.emulator.click_button(*Coordinates.SEARCH_BARBARIANS_BUTTON)  # Click on the search barbarians button

    def IncreaseBarbarianLevel(self):
        self.emulator.click_button(*Coordinates.INCREASE_BARBARIAN_LEVEL)

    def DecreaseBarbarianLevel(self):
        self.emulator.click_button(*Coordinates.DECREASE_BARBARIAN_LEVEL)

    def MarkTheBarbarians(self):
        self.emulator.click_button(*Coordinates.BARBARIANS)  # Click on barbarians

    def ClickAttackButton(self):
        # TODO: Scan and check if attack button popped up on left or right side. Currently its hardcoded to right side which handles 95% of the cases.
        self.emulator.click_button(*Coordinates.ATTACK_BUTTON)  # Click Attack button

    def SelectTroops(self):
        self.emulator.click_button(*Coordinates.SELECT_TROOPS)  # select troops

    def MarchAndStartAttack(self):
        self.emulator.click_button(*Coordinates.START_ATTACK)  # Start the attack

    def IsSearchButtonPresent(self):
        retries = 3
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/SearchButton.png", 189, 458, 356, 518):
                return True
        return False

    def AreTroopsMarching(self):
        retries = 5
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/marching.png", 1235, 209, 1256, 228):
                return True
        return False

    def AreTroopsInCombat(self):
        retries = 3
        for _ in range(retries):
            combat_images = glob.glob("Templates/combat/combat*.png")
            for image_path in combat_images:
                if self.emulator.isImageFound(image_path, 1235, 209, 1256, 228):
                    return True
        return False
