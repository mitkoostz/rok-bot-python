import subprocess
import time
import cv2
import numpy as np
import glob

class GameBot:
    def __init__(self, adb_path='adb', device_ip='127.0.0.1:5555'):
        self.adb_path = adb_path
        self.device_ip = device_ip
        self.device_serial = None

    def connect_device(self):
        result = subprocess.run([self.adb_path, 'connect', self.device_ip], capture_output=True, text=True)
        if 'connected' in result.stdout:
            print("Connected to device.")
            devices_result = subprocess.run([self.adb_path, 'devices'], capture_output=True, text=True)
            devices = [line.split()[0] for line in devices_result.stdout.splitlines() if '\tdevice' in line]
            if devices:
                self.device_serial = devices[0]
                print(f"Using device: {self.device_serial}")
                return True
            else:
                print("No devices found.")
                return False
        else:
            print("Failed to connect to device.")
            return False
    def set_resolution(self, width, height):
        if self.device_serial:
            print(f"Setting resolution to {width}x{height} for device {self.device_serial}")
            result = subprocess.run(
                [self.adb_path, '-s', self.device_serial, 'shell', 'wm', 'size', f'{width}x{height}'],
                text=True,
                capture_output=True
            )
            print("ADB Output:", result.stdout)
            print("ADB Error:", result.stderr)
        else:
            print("No device serial specified.")
    def click_button(self, x, y):
        if self.device_serial:
            subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'input', 'tap', str(x), str(y)])
            print(f"Clicked at coordinates ({x}, {y})")
        else:
            print("No device serial specified.")
    def isImageFound(self, template_path, x_start, y_start, x_end, y_end, accuracyTreshold = 0.6):
        if self.device_serial:
            # Capture screenshot
            result = subprocess.run([self.adb_path, '-s', self.device_serial, 'exec-out', 'screencap', '-p'], capture_output=True)
            screenshot = np.frombuffer(result.stdout, np.uint8)
            screenshot = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)

            # Crop the screenshot to the specified region
            cropped_screenshot = screenshot[y_start:y_end, x_start:x_end]
            cv2.imwrite('saerchRegion.png', cropped_screenshot)

            # Load template
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"Failed to load template image from {template_path}")
                return

            w, h = template.shape[:-1]

            # Match template
            res = cv2.matchTemplate(cropped_screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # Debug information
            #print(f"Template matching results: min_val={min_val}, max_val={max_val}, min_loc={min_loc}, max_loc={max_loc}")
            #cv2.imwrite('captureregion.png', cropped_screenshot)
            #print("Captured region saved as 'captureregion.png'.")

            # If match is found, click the button and save the region
            if max_val > accuracyTreshold:  # Adjust threshold as needed
                top_left = max_loc
                center_x = top_left[0] + w // 2 + x_start
                center_y = top_left[1] + h // 2 + y_start
                #self.click_button(center_x, center_y)

                # Extract and save the region
                bottom_right = (top_left[0] + w, top_left[1] + h)
                region = cropped_screenshot[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                #print(f"IMAGE FOUND! At coordinates ({center_x}, {center_y})")
                return True
            else:
                return False
        else:
            print("No device serial specified.")
    def isInCombat(self):
        retries = 3
        for _ in range(retries):
            combat_images = glob.glob("Templates/combat/combat*.png")
            for image_path in combat_images:
                print(f"Checking {image_path}")
                if self.isImageFound(image_path, 1235, 209, 1256, 228):
                    print(f"Found and clicked {image_path}")
                    return True
        return False
    def isMarching(self):
        retries = 5
        for _ in range(retries):
            if self.isImageFound("Templates/marching.png", 1235, 209, 1256, 228):
                return True
        return False
