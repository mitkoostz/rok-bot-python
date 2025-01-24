from ppadb.client import Client as AdbClient

class ScreenshotCapturer:
    @staticmethod
    def capture_screenshot():
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        if devices:
            device = devices[0]
            print(f"Connected to {device.serial}")
            screenshot = device.screencap()
            with open('screenshot.png', 'wb') as f:
                f.write(screenshot)
            print("Screenshot saved as 'screenshot.png'.")
        else:
            print("No device found. Please check your ADB connection.")
