# echo_test_ping.py

import os
import importlib.util

# Path to your local agent script
agent_path = os.path.join(os.getcwd(), 'echo_local_agent.py')

# Dynamically load the agent script
spec = importlib.util.spec_from_file_location("echo_local_agent", agent_path)
echo_agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(echo_agent)

# Example test input
user_input = "Hello Echo, are you awake?"

# Call the memory agent function (replace with your actual function name if needed)
response = echo_agent.process_input(user_input)

# Output the result
print("Test input:", user_input)
print("Echo's response:", response)