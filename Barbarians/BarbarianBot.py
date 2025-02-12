from Emulator.Cordinates import Coordinates
from Barbarians.TroopsScanner import TroopsScanner
from .BarbarianLevelManager import BarbarianLevelManager
import time
import glob
import random


class BarbarianBot:
    isFirstRun = True
    lastSelectedBarbarianLevel = 0

    def __init__(self, emulator, maximumPercentageThatTroopsAreAllowedToDecrease, checkForHealingIntervalSeconds, initialBarbarianLevelStart = 11, maxBarbLevel = 17):
        self.emulator = emulator
        self.NumberOfTroopGroups = 3
        self.troopsScanner = TroopsScanner(emulator)
        self.BarbarianManager = BarbarianLevelManager(emulator)
        self.maximumPercentageThatTroopsAreAllowedToDecrease = maximumPercentageThatTroopsAreAllowedToDecrease
        self.checkForHealingIntervalSeconds = checkForHealingIntervalSeconds
        self.checkForHealingLastExecutionTime = time.time()
        self.initialBarbarianLevelStart = initialBarbarianLevelStart
        self.maxBarbLevel = maxBarbLevel

    def run_bot(self):
        while True:
            for troop_group in range(1, self.NumberOfTroopGroups + 1):
                isMarching = self.AreTroopsMarching(troop_group)
                isInCombat = self.AreTroopsInCombat(troop_group)
                #print("Troop Group: " + str(troop_group) + "|Marching: " + str(isMarching))
                #print("Troop Group: " + str(troop_group) + "|Combat: " + str(isInCombat))
                time.sleep(0.1)

                if not isMarching and not isInCombat:
                    print("Troop Group: " + str(troop_group) + "is free. Performing barbarian attack.")
                    self.AttackBarbarians(troop_group)

                if isInCombat or isMarching:
                    continue

                # Check if troops are decreased and need refilling
                """
                current_time = time.time()
                if current_time - self.checkForHealingLastExecutionTime >= self.checkForHealingIntervalSeconds:
                    needHealing = self.troopsScanner.AreTroopsDecreased(self.maximumPercentageThatTroopsAreAllowedToDecrease)
                    if needHealing is True:
                        # TODO: Implement healing troops and refilling new troop group
                        print("Troops are decreased. Healing is needed!!!!!!!!!.")
                    self.checkForHealingLastExecutionTime = current_time
                    """

    def AttackBarbarians(self, troop_group):
        self.ClickSearchButton()
        time.sleep(1)
        if BarbarianBot.isFirstRun:
            self.SetBarbarianLevel(self.initialBarbarianLevelStart)

        currentBarbiarianLevel = self.BarbarianManager.get_current_selected_barbarian_level()
        print("Current Barbarian Level: " + str(currentBarbiarianLevel))
        print("Last Attacked Barbarian Level: " + str(BarbarianBot.lastSelectedBarbarianLevel))
        requestedBarbarianLevel = currentBarbiarianLevel

        if requestedBarbarianLevel > self.maxBarbLevel:
            requestedBarbarianLevel = self.initialBarbarianLevelStart

        # Ensure each troop group fights a different barbarian level
        if BarbarianBot.lastSelectedBarbarianLevel == requestedBarbarianLevel:
            requestedBarbarianLevel += random.choice([-2, -1, 1, 2])

        print("New Barbarian Level: " + str(requestedBarbarianLevel))

        self.SetBarbarianLevel(requestedBarbarianLevel)
        time.sleep(1)
        self.SearchForBarbarians()
        time.sleep(1)

        # Handle barbarians not found on the map
        isSearchButtonPresent = self.IsSearchButtonPresent()
        time.sleep(1)
        print("Search button present: " + str(isSearchButtonPresent))
        if isSearchButtonPresent:
            while self.IsSearchButtonPresent():
                print("Troop Group: " +str(troop_group) + " Barbarian level: " + str(currentBarbiarianLevel))
                if requestedBarbarianLevel < self.maxBarbLevel:
                    self.IncreaseBarbarianLevel()
                    requestedBarbarianLevel += 1
                    if requestedBarbarianLevel == BarbarianBot.lastSelectedBarbarianLevel:
                        requestedBarbarianLevel += 1
                    print("Barbarians level increased to: " + str(requestedBarbarianLevel))
                else:
                    requestedBarbarianLevel = self.initialBarbarianLevelStart
                    self.SetBarbarianLevel(self.initialBarbarianLevelStart)
                time.sleep(0.3)
                self.SearchForBarbarians()
                time.sleep(1)

        if isSearchButtonPresent:
            time.sleep(2)
        else:
            time.sleep(1)
        self.MarkTheBarbarians()
        time.sleep(0.5)
        self.ClickAttackButton()
        time.sleep(0.5)
        self.SelectTroops(troop_group)
        time.sleep(0.5)
        self.MarchAndStartAttack(troop_group)
        BarbarianBot.lastSelectedBarbarianLevel = requestedBarbarianLevel
        BarbarianBot.isFirstRun = False
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

    def SelectTroops(self, troop_group):
        print("Selecting Troop Group: " + str(troop_group))
        if troop_group == 1:
            self.emulator.click_button(*Coordinates.SELECT_TROOPS_FIRST)
        if troop_group == 2:
            self.emulator.click_button(*Coordinates.SELECT_TROOPS_SECOND)
        if troop_group == 3:
            self.emulator.click_button(*Coordinates.SELECT_TROOPS_THIRTH)

    def MarchAndStartAttack(self, troop_group):
        if troop_group == 1:
            self.emulator.click_button(*Coordinates.START_ATTACK)
        if troop_group == 2:
            self.emulator.click_button(*Coordinates.START_ATTACK_SECOND)
        if troop_group == 3:
            self.emulator.click_button(*Coordinates.START_ATTACK_THIRTH)

    def IsSearchButtonPresent(self):
        retries = 3
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/SearchButton.png", *Coordinates.SEARCH_BUTTON_COORDINATES_RIGHT_SIDE):
                return True
        return False

    def AreTroopsMarching(self, troop_group):
        if troop_group == 1:
            coordinates = Coordinates.TROOPS_STATUS_ICON_FIRST
        elif troop_group == 2:
            coordinates = Coordinates.TROOPS_STATUS_ICON_SECOND
        elif troop_group == 3:
            coordinates = Coordinates.TROOPS_STATUS_ICON_THIRTH
        else:
            raise ValueError("Invalid troop group")

        x_start, y_start, x_end, y_end = coordinates
        retries = 5
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/marching.png", x_start, y_start, x_end, y_end) or \
               self.emulator.isImageFound("Templates/marchingHome.png", x_start, y_start, x_end, y_end):
                return True
        return False

    def AreTroopsInCombat(self, troop_group):
        if troop_group == 1:
            coordinates = Coordinates.TROOPS_STATUS_ICON_FIRST
        elif troop_group == 2:
            coordinates = Coordinates.TROOPS_STATUS_ICON_SECOND
        elif troop_group == 3:
            coordinates = Coordinates.TROOPS_STATUS_ICON_THIRTH
        else:
            raise ValueError("Invalid troop group")

        x_start, y_start, x_end, y_end = coordinates
        retries = 3
        for _ in range(retries):
            combat_images = glob.glob("Templates/combat/combat*.png")
            for image_path in combat_images:
                if self.emulator.isImageFound(image_path, x_start, y_start, x_end, y_end):
                    return True
        return False

    def SetBarbarianLevel(self, desired_level):
        currentBarbarianLevel = self.BarbarianManager.get_current_selected_barbarian_level()
        while currentBarbarianLevel < desired_level:
            self.IncreaseBarbarianLevel()
            currentBarbarianLevel += 1
            print("Barbarians level increased to: " + str(currentBarbarianLevel))
            time.sleep(0.5)

        while currentBarbarianLevel > desired_level:
            self.DecreaseBarbarianLevel()
            currentBarbarianLevel -= 1
            print("Barbarians level decreased to: " + str(currentBarbarianLevel))
            time.sleep(0.5)
