from BlueStacksAppChecker import BlueStacksAppChecker
from ADBConnection import GameBot
from ScreenshotCapturer import ScreenshotCapturer
from ColorConstants import ColorConstants
import time

# Main function to check BlueStacks, ADB connection, and capture screenshot
def main():
    if BlueStacksAppChecker.is_bluestacks_running():
        print("BlueStacks is running.")
        bot = GameBot()
        if bot.connect_device():
            ScreenshotCapturer.capture_screenshot()

            while True:
                bot.set_resolution(1280, 720)
                isMarching = bot.isMarching()
                isInCombat = bot.isInCombat()
                print("Marching: " + str(isMarching))
                print("Combat: " + str(isInCombat))
                time.sleep(1)

                if isMarching == False and isInCombat == False:
                    time.sleep(2)
                    bot.click_button(58, 541) # Click on the search bar
                    time.sleep(1)
                    bot.click_button(289, 488) # Click on the search barbarians button
                    time.sleep(2.1)
                    bot.click_button(690, 360) # Click on barbarians
                    time.sleep(0.3)
                    bot.click_button(886, 460) # Click Atack button
                    time.sleep(0.4)
                    bot.click_button(1213, 224) # select troops
                    time.sleep(0.3)
                    bot.click_button(1030, 300) # Start the attack
                    time.sleep(1)
                while bot.isMarching():
                    print("Marching to troops which will be attacked.")
                    time.sleep(1)
                print("Marching is done.")
                time.sleep(2)
                while bot.isInCombat():
                    print("In combat.")
                    time.sleep(1)
    else:
        print("BlueStacks is not running. Please start BlueStacks.")

if __name__ == "__main__":
    main()
