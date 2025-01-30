from Emulator.ImageNumberExtractor import ImageNumberExtractor


class BarbarianLevelManager:
    def __init__(self, emulator):
        self.emulator = emulator

    def get_current_selected_barbarian_level(self):
        image = self.emulator.capture_region(128, 366, 426, 387)
        currentBarbLevel = ImageNumberExtractor.get_integer_from_image(image)
        print(f"Current selected barbarian level: {currentBarbLevel}")
        return currentBarbLevel

    def increaseLevel(self):
        self.emulator.click_button(409, 401)

    def decreaseLevel(self):
        self.emulator.click_button(135, 401)
