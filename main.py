from BlueStacksAppChecker import BlueStacksAppChecker
from EmulatorController import EmulatorController
from BarbarianBot import BarbarianBot


def main():
    startBot = True
    if BlueStacksAppChecker.is_bluestacks_running():
        print("BlueStacks is running.")
        emulator = EmulatorController()
        barbarian_bot = BarbarianBot(emulator)
        if emulator.connect_device():
            emulator.set_resolution(1280, 720)
            if startBot:
                barbarian_bot.run_bot()
            else:
                print("Bot will not start!!!")
    else:
        print("BlueStacks is not running. Please start BlueStacks.")


if __name__ == "__main__":
    main()
