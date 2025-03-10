import subprocess
import cv2
import numpy as np
import time


class EmulatorController:
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
            #print(f"Clicked at coordinates ({x}, {y})")
        else:
            print("No device serial specified.")

    def isImageFound(self, template_path, x_start, y_start, x_end, y_end, filename='IsImageFoundRegion.png', accuracyThreshold=0.6):
        if self.device_serial:
            # Capture screenshot
            result = subprocess.run([self.adb_path, '-s', self.device_serial, 'exec-out', 'screencap', '-p'], capture_output=True)
            screenshot = np.frombuffer(result.stdout, np.uint8)
            screenshot = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)

            # Crop the screenshot to the specified region
            cropped_screenshot = screenshot[y_start:y_end, x_start:x_end]
            cv2.imwrite(f'OutputImages/{filename}', cropped_screenshot)

            # Load template
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"Failed to load template image from {template_path}")
                return

            w, h = template.shape[:-1]

            # Match template
            res = cv2.matchTemplate(cropped_screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > accuracyThreshold:  # Adjust threshold as needed
                return True
            else:
                return False
        else:
            print("No device serial specified.")

    def capture_region(self, x_start, y_start, x_end, y_end, filename='CapturedRegion.png'):
        if self.device_serial:
            # Capture screenshot
            result = subprocess.run([self.adb_path, '-s', self.device_serial, 'exec-out', 'screencap', '-p'], capture_output=True)
            screenshot = np.frombuffer(result.stdout, np.uint8)
            screenshot = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)
            # Crop the screenshot to the specified region
            cropped_screenshot = screenshot[y_start:y_end, x_start:x_end]
            cv2.imwrite(f'OutputImages/{filename}', cropped_screenshot)

            return cropped_screenshot
        else:
            print("No device serial specified.")
            return None

    def capture_screenshot(self, filename='screenshot.png'):
        if self.device_serial:
            # Capture screenshot
            result = subprocess.run([self.adb_path, '-s', self.device_serial, 'exec-out', 'screencap', '-p'], capture_output=True)
            screenshot = np.frombuffer(result.stdout, np.uint8)
            screenshot = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)
            # Save the screenshot to a file
            cv2.imwrite(filename, screenshot)
            return screenshot
        else:
            print("No device serial specified.")
            return None
