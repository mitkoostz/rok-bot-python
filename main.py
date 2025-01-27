from BlueStacksAppChecker import BlueStacksAppChecker
from EmulatorController import EmulatorController
from BarbarianBot import BarbarianBot


def main():
    startBot = True
    if BlueStacksAppChecker.is_bluestacks_running():
        print("BlueStacks is running.")
        emulator = EmulatorController()
        if emulator.connect_device():
            emulator.set_resolution(1280, 720)
            barbarian_bot = BarbarianBot(emulator)
            if startBot is False:
                # Test region start

                # Test region end
                print("Bot will not start as it is in DEBUG MODE")
            else:
                barbarian_bot.run_bot()
    else:
        print("BlueStacks is not running. Please start BlueStacks.")


if __name__ == "__main__":
    main()
