from Emulator.Cordinates import Coordinates
from Barbarians.TroopsScanner import TroopsScanner
from .BarbarianLevelManager import BarbarianLevelManager
import time
import glob
import random


class BarbarianBot:
    isFirstBarbarianFight = True
    lastSelectedBarbarianLevels = [0, 0, 0]

    def __init__(self, emulator, maxTroopDecreasePercentage, healingCheckInterval, initialBarbarianLevel=11, maxBarbLevel=17):
        self.emulator = emulator
        self.StartingTroopGroups = [1, 2, 3]
        self.NumberOfTroopGroups = []
        self.TroopGroupsButtonMapping = {}
        self.troopsScanner = TroopsScanner(emulator)
        self.BarbarianManager = BarbarianLevelManager(emulator)
        self.maxTroopDecreasePercentage = maxTroopDecreasePercentage
        self.healingCheckInterval = healingCheckInterval
        self.lastHealingCheckTime = time.time()
        self.initialBarbarianLevel = initialBarbarianLevel
        self.maxBarbLevel = maxBarbLevel

    def run_bot(self):
        while True:
            self.update_troop_groups()
            if not self.NumberOfTroopGroups:
                print(f"No troop groups found. Spawning troop groups: {self.StartingTroopGroups}")
                self.spawn_troop_group(1, self.StartingTroopGroups[-1])
                continue

            for troop_group, isAlive in self.NumberOfTroopGroups:
                if not isAlive:
                    print(f"Troop Group: {troop_group} is DEAD. Skipping this group.")
                    continue

                if not self.AreTroopsMarching(troop_group) and not self.AreTroopsInCombat(troop_group):
                    print(f"Troop Group: {troop_group} is free. Performing barbarian attack.")
                    self.AttackBarbarians(troop_group)

            if len(self.NumberOfTroopGroups) < len(self.StartingTroopGroups):
                print("Troop groups are missing. Spawning one of the missing groups.")
                self.spawn_one_missing_troop_group()

    def update_troop_groups(self):
        numberOfTroopGroups = self.troopsScanner.GetNumberOfTroopGroups()
        if numberOfTroopGroups is None:
            return
        self.NumberOfTroopGroups = [(i, not self.AreTroopsDead(i)) for i in range(1, numberOfTroopGroups + 1)]
        print(f"All Troop Groups: {self.NumberOfTroopGroups}")

    def spawn_one_missing_troop_group(self):
        missingTroopGroups = self.get_missing_troop_groups()
        for troop_group in self.StartingTroopGroups:
            if len(self.NumberOfTroopGroups) >= len(self.StartingTroopGroups):
                continue
            quick_button = self.TroopGroupsButtonMapping.get(troop_group, missingTroopGroups[0])
            print(f"Spawning troop group: {troop_group} with quick button: {quick_button}")
            self.spawn_troop_group(troop_group, quick_button)
            return

    def get_missing_troop_groups(self):
        mapped_values = set(self.TroopGroupsButtonMapping.values())
        starting_values = set(self.StartingTroopGroups)
        return list(starting_values - mapped_values)

    def spawn_troop_group(self, troop_group, quick_button):
        self.RefreshOpenWorldView()
        self.emulator.click_button(400, 350)
        time.sleep(1)
        if not self.emulator.isImageFound("Templates/MarchButton.png", 721, 386, 923, 458):
            return
        time.sleep(1)
        self.emulator.click_button(817, 420)
        time.sleep(1)
        self.emulator.click_button(1000, 142)
        time.sleep(1)
        self.emulator.click_button(1103, 258 + (quick_button - 1) * 55)
        time.sleep(1)
        #TODO: Check if troop group is spawned, if not close this window
        self.emulator.click_button(920, 637)
        self.NumberOfTroopGroups.append((troop_group, True))
        self.TroopGroupsButtonMapping[troop_group] = quick_button
        time.sleep(1)

    def AttackBarbarians(self, troop_group):
        self.ClickSearchButton()
        time.sleep(1)
        if BarbarianBot.isFirstBarbarianFight:
            self.SetBarbarianLevel(self.initialBarbarianLevel)
            print(f"First bot run - Initial Barbarian Level: {self.initialBarbarianLevel}")
            BarbarianBot.isFirstBarbarianFight = False

        requestedBarbarianLevel = self.get_unique_barbarian_level(self.BarbarianManager.get_current_selected_barbarian_level(), BarbarianBot.lastSelectedBarbarianLevels)
        self.SetBarbarianLevel(requestedBarbarianLevel)
        time.sleep(1)
        self.SearchForBarbarians()
        time.sleep(1)

        if self.handle_barbarians_not_found(requestedBarbarianLevel):
            time.sleep(2)
        else:
            time.sleep(1)

        self.MarkTheBarbarians()
        time.sleep(0.5)
        if self.ClickAttackButton():
            time.sleep(0.5)
            self.SelectTroops(troop_group)
            time.sleep(0.5)
            self.MarchAndStartAttack(troop_group)
            BarbarianBot.lastSelectedBarbarianLevels[troop_group - 1] = requestedBarbarianLevel
            time.sleep(1)

    def handle_barbarians_not_found(self, requestedBarbarianLevel):
        notAvailableLevels = []
        while self.IsSearchButtonPresent():
            notAvailableLevels.append(requestedBarbarianLevel)
            requestedBarbarianLevel = self.get_unique_barbarian_level(requestedBarbarianLevel, randomize=False, notAvailableLevels=notAvailableLevels)
            self.SetBarbarianLevel(requestedBarbarianLevel)
            time.sleep(0.3)
            self.SearchForBarbarians()
            time.sleep(1)
        return self.IsSearchButtonPresent()

    def get_unique_barbarian_level(self, requestedBarbarianLevel, notAvailableLevels, randomize=False):
        if requestedBarbarianLevel is None:
            requestedBarbarianLevel = self.initialBarbarianLevel
        if notAvailableLevels is None or len(notAvailableLevels) > 15:
            return self.initialBarbarianLevel
        valid_levels = set(range(self.initialBarbarianLevel, self.maxBarbLevel + 1))
        available_levels = list(valid_levels - set(BarbarianBot.lastSelectedBarbarianLevels))
        print(f"Previously selected barb levels: {BarbarianBot.lastSelectedBarbarianLevels}")
        print(f"Available barb levels to attack: {available_levels}")
        if notAvailableLevels:
            available_levels = [level for level in available_levels if level not in notAvailableLevels]
        if not available_levels:
            return self.initialBarbarianLevel
        return random.choice(available_levels) if randomize else min(available_levels)

    def ClickSearchButton(self):
        self.emulator.click_button(*Coordinates.SEARCH_BAR)

    def SearchForBarbarians(self):
        self.emulator.click_button(*Coordinates.SEARCH_BARBARIANS_BUTTON)

    def IncreaseBarbarianLevel(self):
        self.emulator.click_button(*Coordinates.INCREASE_BARBARIAN_LEVEL)

    def DecreaseBarbarianLevel(self):
        self.emulator.click_button(*Coordinates.DECREASE_BARBARIAN_LEVEL)

    def MarkTheBarbarians(self):
        self.emulator.click_button(*Coordinates.BARBARIANS)

    def ClickAttackButton(self):
        self.emulator.click_button(*Coordinates.ATTACK_BUTTON)
        time.sleep(0.3)
        if self.IsNewTroopsButtonPresent():
            return True
        self.RefreshOpenWorldView()
        return False

    def RefreshOpenWorldView(self):
        #TODO: Implement that with image scan and be sure you awlays end up in open world view and not the city view
        self.emulator.click_button(*Coordinates.CASTLE_OPEN_AREA_BUTTON)
        time.sleep(2.5)
        self.emulator.click_button(*Coordinates.CASTLE_OPEN_AREA_BUTTON)
        time.sleep(1)

    def SelectTroops(self, troop_group):
        print(f"Selecting Troop Group: {troop_group}")
        coordinates = {
            1: Coordinates.SELECT_TROOPS_FIRST,
            2: Coordinates.SELECT_TROOPS_SECOND,
            3: Coordinates.SELECT_TROOPS_THIRD
        }
        self.emulator.click_button(*coordinates[troop_group])

    def MarchAndStartAttack(self, troop_group):
        coordinates = {
            1: Coordinates.START_ATTACK,
            2: Coordinates.START_ATTACK_SECOND,
            3: Coordinates.START_ATTACK_THIRD
        }
        self.emulator.click_button(*coordinates[troop_group])

    def IsSearchButtonPresent(self):
        return any(self.emulator.isImageFound("Templates/SearchButton.png", *Coordinates.SEARCH_BUTTON_COORDINATES_RIGHT_SIDE) for _ in range(3))

    def IsNewTroopsButtonPresent(self):
        return any(self.emulator.isImageFound("Templates/NewTroopsButton.png", *Coordinates.New_Troops_Button) for _ in range(3))

    def AreTroopsMarching(self, troop_group):
        coordinates = {
            1: Coordinates.TROOPS_STATUS_ICON_FIRST,
            2: Coordinates.TROOPS_STATUS_ICON_SECOND,
            3: Coordinates.TROOPS_STATUS_ICON_THIRD
        }
        x_start, y_start, x_end, y_end = coordinates[troop_group]
        return any(self.emulator.isImageFound("Templates/marching.png", x_start, y_start, x_end, y_end) or
                   self.emulator.isImageFound("Templates/marchingHome.png", x_start, y_start, x_end, y_end) for _ in range(3))

    def AreTroopsDead(self, troop_group):
        coordinates = {
            1: Coordinates.TROOPS_STATUS_ICON_FIRST,
            2: Coordinates.TROOPS_STATUS_ICON_SECOND,
            3: Coordinates.TROOPS_STATUS_ICON_THIRD
        }
        x_start, y_start, x_end, y_end = coordinates[troop_group]
        return any(self.emulator.isImageFound("Templates/dead.png", x_start, y_start, x_end, y_end) for _ in range(3))

    def AreTroopsInCombat(self, troop_group):
        coordinates = {
            1: Coordinates.TROOPS_STATUS_ICON_FIRST,
            2: Coordinates.TROOPS_STATUS_ICON_SECOND,
            3: Coordinates.TROOPS_STATUS_ICON_THIRD
        }
        x_start, y_start, x_end, y_end = coordinates[troop_group]
        combat_images = glob.glob("Templates/combat/combat.png")
        return any(self.emulator.isImageFound(image_path, x_start, y_start, x_end, y_end) for image_path in combat_images for _ in range(3))

    def SetBarbarianLevel(self, desired_level):
        currentBarbarianLevel = self.BarbarianManager.get_current_selected_barbarian_level() or self.initialBarbarianLevel
        while currentBarbarianLevel < desired_level:
            self.IncreaseBarbarianLevel()
            currentBarbarianLevel += 1
            print(f"Barbarians level increased to: {currentBarbarianLevel}")
            time.sleep(0.5)
        while currentBarbarianLevel > desired_level:
            self.DecreaseBarbarianLevel()
            currentBarbarianLevel -= 1
            print(f"Barbarians level decreased to: {currentBarbarianLevel}")
            time.sleep(0.5)
        print(f"Barbarian level is set to: {currentBarbarianLevel}")
