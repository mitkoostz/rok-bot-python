from BlueStackEmulator.BlueStacksAppChecker import BlueStacksAppChecker
from Emulator.EmulatorController import EmulatorController
from Barbarians.BarbarianBot import BarbarianBot
from Barbarians.BarbarianLevelManager import BarbarianLevelManager
from Emulator.Cordinates import Coordinates
import time
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    resolution_width = config.getint('Emulator', 'ResolutionWidth')
    resolution_height = config.getint('Emulator', 'ResolutionHeight')

    bluestacks_executable_name = config['BlueStacks']['ExecutableName']
    max_troop_decrease_percentage = config.getint('BarbarianBotSettings', 'MaximumPercentageThatTroopsAreAllowedToDecrease')
    check_for_healing_interval_seconds = config.getint('BarbarianBotSettings', 'CheckForHealingIntervalSeconds')
    initial_barbarian_level = config.getint('BarbarianBotSettings', 'InitialBarbarianLevelStart')

    startBot = True
    if BlueStacksAppChecker.is_bluestacks_running(bluestacks_executable_name):
        print("BlueStacks is running.")
        emulator = EmulatorController()
        if emulator.connect_device():
            emulator.set_resolution(resolution_width, resolution_height)
            barbarian_bot = BarbarianBot(emulator, max_troop_decrease_percentage, check_for_healing_interval_seconds)
            if startBot is False:
                # Test region start
                count = 1
                while True:
                    emulator.capture_region(*Coordinates.TROOPS_STATUS_ICON_FIRST, "FirstGroupStatus.png")
                    count += 1
                    time.sleep(2)
                # Test region end
                print("Bot will not start as it is in DEBUG MODE")
            else:
                barbarian_bot.run_bot()
                print("Barbarian bot started.")
    else:
        print("BlueStacks is not running. Please start BlueStacks.")


if __name__ == "__main__":
    main()
