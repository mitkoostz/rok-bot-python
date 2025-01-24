import psutil

class BlueStacksAppChecker:
    @staticmethod
    def is_bluestacks_running():
        for process in psutil.process_iter(['pid', 'name']):
            if 'BlueStacksAppplayerWeb.exe' in process.info['name']:
                return True
        return False
