import os
import subprocess
from datetime import datetime

# Paths (update if needed)
utility_script_name = "echo_autonomous_example.py"
utility_script_path = os.path.join(os.path.dirname(__file__), utility_script_name)
task_name = "Echo_Autonomous_Example"

# 1. Create a simple utility script
utility_code = '''
from datetime import datetime

log_path = "D:/Echo_Memory_Archive/Logs/autonomous_example_log.txt"

with open(log_path, "a") as log_file:
    log_file.write(f"[{datetime.now()}] Echo ran autonomous utility script successfully.\\n")
'''

with open(utility_script_path, "w") as f:
    f.write(utility_code.strip())

print(f"Utility script created at: {utility_script_path}")

# 2. Schedule the script using Windows Task Scheduler
# Set it to run once, 1 minute from now
run_time = (datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)).strftime("%H:%M")
run_date = datetime.now().strftime("%Y-%m-%d")

command = f'''
schtasks /Create /SC ONCE /TN "{task_name}" /TR "python {utility_script_path}" /ST {run_time} /SD {run_date} /F
'''

try:
    subprocess.run(command, shell=True, check=True)
    print(f"Scheduled task '{task_name}' for {run_date} at {run_time}")
except subprocess.CalledProcessError as e:
    print(f"Error scheduling task: {e}")