import psutil


class BlueStacksAppChecker:
    @staticmethod
    def is_bluestacks_running(executableName):
        for process in psutil.process_iter(['pid', 'name']):
            if executableName in process.info['name']:
                return True
        return False
