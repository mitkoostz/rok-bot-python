from Emulator.Cordinates import Coordinates
import time
from Emulator.ImageNumberExtractor import ImageNumberExtractor


class TroopsScanner:
    def __init__(self, emulator):
        self.emulator = emulator
        self.InitialTroopsNumber = self.ScanCurrentNumberOfTroops()
        print("Initial/Starting Troops number:", self.InitialTroopsNumber)

    def ScanCurrentNumberOfTroops(self):
        time.sleep(1)
        self.emulator.click_button(*Coordinates.TroopsInformationOpenButton)
        time.sleep(1)
        troopsNumberImage = self.emulator.capture_region(480, 225, 670, 260)
        troopsNumber = ImageNumberExtractor.get_comma_separated_decimal(troopsNumberImage)
        print("Alive Troops number:", troopsNumber)
        time.sleep(1)
        self.emulator.click_button(*Coordinates.TroopsInformationCloseButton)
        return troopsNumber

    def AreTroopsDecreased(self, percentage_threshold):
        currentTroopsNumber = self.ScanCurrentNumberOfTroops()
        if currentTroopsNumber is None:
            return False
        threshold = self.InitialTroopsNumber * (1 - percentage_threshold / 100)
        return currentTroopsNumber < threshold

