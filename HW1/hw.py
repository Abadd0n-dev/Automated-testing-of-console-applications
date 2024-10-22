import subprocess

def check_command_output(command, search_text):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and search_text in result.stdout
    except Exception:
        return False