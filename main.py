import psutil
import time

def list_processes():
    print(f"\033[92;42m{'PID':<10}{'Name':<50}{'CPU Usage (%)':<15}{'Memory Usage (%)':<15}\033[0m")
    print("-" * 91)

    system_paths = ['C:\\Windows\\System32', 'C:\\Windows\\']
    current_user = psutil.Process().username()

    # Initialize CPU usage to avoid immediate zero readings
    psutil.cpu_percent(interval=0.1)
    time.sleep(0.1)  # Short sleep to allow CPU usage to be recorded

    # Iterate over processes
    for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "exe", "username", "status"]):
        try:
            exe_path = process.info["exe"] if process.info["exe"] else ""
            username = process.info.get("username", "")
            if (process.info["status"] == psutil.STATUS_RUNNING and 
                    username == current_user and 
                    not any(exe_path.startswith(path) for path in system_paths)):
                
                # Get the actual CPU usage with a slight delay
                time.sleep(0.1)  # Allow time for CPU usage to change
                cpu_usage = process.cpu_percent(interval=0.1)
                memory_usage = process.memory_percent()
                print(f"\033[94m{process.info['pid']:<10}\033[0m\033[95m{process.info['name']:<50}\033[0m{cpu_usage:<15}\033[96m{memory_usage:<15}\033[0m")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue 

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        print(f"Terminating process {pid} ({process.name()})...")
        process.terminate()
        process.wait(timeout=3)
        print(f"Process {pid} ({process.name()}) has been terminated.")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} does not exist.")
    except psutil.AccessDenied:
        print(f"Permission denied to terminate process with PID {pid}.")
    except Exception as e:
        print(f"An error occurred: {e}")

try:
    list_processes()
    kill_pid = int(input("Enter the PID of the process you want to terminate: "))
    kill_process(kill_pid)
except KeyboardInterrupt:
    print("\nOops! There is some interruption, this is awkward XD.")
except ValueError:
    print("Invalid PID entered. Please enter a valid PID.")
