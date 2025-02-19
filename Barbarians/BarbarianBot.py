from Emulator.Cordinates import Coordinates
from Barbarians.TroopsScanner import TroopsScanner
from .BarbarianLevelManager import BarbarianLevelManager
import time
import glob
import random


class BarbarianBot:
    isFirstRun = True
    lastSelectedBarbarianLevels = [0, 0, 0]

    def __init__(self, emulator, maximumPercentageThatTroopsAreAllowedToDecrease, checkForHealingIntervalSeconds, initialBarbarianLevelStart = 11, maxBarbLevel = 17):
        self.emulator = emulator
        self.NumberOfTroopGroups = []
        self.troopsScanner = TroopsScanner(emulator)
        self.BarbarianManager = BarbarianLevelManager(emulator)
        self.maximumPercentageThatTroopsAreAllowedToDecrease = maximumPercentageThatTroopsAreAllowedToDecrease
        self.checkForHealingIntervalSeconds = checkForHealingIntervalSeconds
        self.checkForHealingLastExecutionTime = time.time()
        self.initialBarbarianLevelStart = initialBarbarianLevelStart
        self.maxBarbLevel = maxBarbLevel

    def run_bot(self):
        while True:
            self.update_troop_groups()
            if (len(self.NumberOfTroopGroups) == 0):
                print("No troop groups found. Exiting the bot.")
                break
            for troop_group, isAlive in self.NumberOfTroopGroups:
                if not isAlive:
                    print("Troop Group: " + str(troop_group) + " is DEAD. Skipping this group.")
                    continue

                isMarching = self.AreTroopsMarching(troop_group)
                isInCombat = self.AreTroopsInCombat(troop_group)
                time.sleep(0.1)

                if not isMarching and not isInCombat:
                    print("Troop Group: " + str(troop_group) + " is free. Performing barbarian attack.")
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

    def update_troop_groups(self):
        self.NumberOfTroopGroups = []
        numberOfTroopGroups = self.troopsScanner.GetNumberOfTroopGroups()
        if numberOfTroopGroups is None:
            return
        for i in range(1, numberOfTroopGroups + 1):
            isAlive = not self.AreTroopsDead(i)
            self.NumberOfTroopGroups.append((i, isAlive))
        print(f"All Troop Groups: {self.NumberOfTroopGroups}")

    def AttackBarbarians(self, troop_group):
        self.ClickSearchButton()
        time.sleep(1)
        if BarbarianBot.isFirstRun:
            self.SetBarbarianLevel(self.initialBarbarianLevelStart)

        print("Last Attacked Barbarian Levels: " + str(BarbarianBot.lastSelectedBarbarianLevels))
        requestedBarbarianLevel = self.BarbarianManager.get_current_selected_barbarian_level()
        requestedBarbarianLevel = self.get_unique_barbarian_level(requestedBarbarianLevel)
        self.SetBarbarianLevel(requestedBarbarianLevel)

        time.sleep(1)
        self.SearchForBarbarians()
        time.sleep(1)

        # Handle barbarians not found on the map
        isSearchButtonPresent = self.IsSearchButtonPresent()
        time.sleep(1)
        print("Search button present: " + str(isSearchButtonPresent))
        if isSearchButtonPresent:
            notAvailableLevels = []
            while self.IsSearchButtonPresent():
                notAvailableLevels.append(requestedBarbarianLevel)
                requestedBarbarianLevel = self.get_unique_barbarian_level(requestedBarbarianLevel, randomize=False, notAvailableLevels=notAvailableLevels)
                self.SetBarbarianLevel(requestedBarbarianLevel)
                time.sleep(0.3)
                self.SearchForBarbarians()
                time.sleep(1)

        if isSearchButtonPresent:
            time.sleep(2)
        else:
            time.sleep(1)
        self.MarkTheBarbarians()
        time.sleep(0.5)
        selected = self.ClickAttackButton()
        if not selected:
            return

        time.sleep(0.5)
        self.SelectTroops(troop_group)
        time.sleep(0.5)
        self.MarchAndStartAttack(troop_group)
        BarbarianBot.lastSelectedBarbarianLevels[troop_group - 1] = requestedBarbarianLevel
        BarbarianBot.isFirstRun = False
        time.sleep(1)

    def get_unique_barbarian_level(self, requestedBarbarianLevel, randomize=False, notAvailableLevels=None):
        if requestedBarbarianLevel is None:
            requestedBarbarianLevel = self.initialBarbarianLevelStart

        valid_levels = set(range(self.initialBarbarianLevelStart, self.maxBarbLevel + 1))
        last_selected_levels = set(BarbarianBot.lastSelectedBarbarianLevels)
        available_levels = list(valid_levels - last_selected_levels)
        if notAvailableLevels is not None:
            print("Not available levels: " + str(notAvailableLevels))
            available_levels = [level for level in available_levels if level not in notAvailableLevels]
        print("Available levels for selection: " + str(available_levels))

        if not available_levels:
            return self.initialBarbarianLevelStart

        if randomize:
            choice = random.choice(available_levels)
            print("Selecting random from possible levels: " + str(choice))
            return choice

        print("Selecting lowest possible level: " + str(min(available_levels)))
        return min(available_levels)

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
        self.emulator.click_button(*Coordinates.ATTACK_BUTTON)
        time.sleep(0.3)
        if self.IsNewTroopsButtonPresent():
            return True
        self.RefreshOpenWorldView()
        return False

    def RefreshOpenWorldView(self):
        # TODO: Make this function to scan image and always finish with open world view
        self.emulator.click_button(*Coordinates.CASTLE_OPEN_AREA_BUTTON)
        time.sleep(2.5)
        self.emulator.click_button(*Coordinates.CASTLE_OPEN_AREA_BUTTON)

    def SelectTroops(self, troop_group):
        #TODO: Check if the troops that are for selection are not decreased troop_group because of deead troop group
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

    def IsNewTroopsButtonPresent(self):
        retries = 3
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/NewTroopsButton.png", *Coordinates.New_Troops_Button):
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
        retries = 3
        for _ in range(retries):
            if self.emulator.isImageFound("Templates/marching.png", x_start, y_start, x_end, y_end) or \
               self.emulator.isImageFound("Templates/marchingHome.png", x_start, y_start, x_end, y_end):
                return True
        return False

    def AreTroopsDead(self, troop_group):
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
            if self.emulator.isImageFound("Templates/dead.png", x_start, y_start, x_end, y_end):
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
            #combat_images = glob.glob("Templates/combat/combat*.png")
            combat_images = glob.glob("Templates/combat/combat.png")
            for image_path in combat_images:
                if self.emulator.isImageFound(image_path, x_start, y_start, x_end, y_end):
                    return True
        return False

    def SetBarbarianLevel(self, desired_level):
        currentBarbarianLevel = self.BarbarianManager.get_current_selected_barbarian_level()
        if currentBarbarianLevel is None:
            currentBarbarianLevel = self.initialBarbarianLevelStart
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

        print("Barbarian level is set to: " + str(currentBarbarianLevel))

