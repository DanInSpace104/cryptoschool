import platform
import subprocess


def clear_screen():
    """Clears the terminal screen."""
    command = "cls" if platform.system().lower() == "windows" else "clear"
    return subprocess.call(command) == 0


def wait_for_enter_and_clear():
    input('Press Enter to continue...')
    clear_screen()
