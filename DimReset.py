import os
import shutil
from os.path import exists
import nbtlib
import time

from ampapi.modules.ADS import ADS
from ampapi.modules.CommonAPI import CommonAPI

import DragonReset


# Define your reset functions here
def reset_mining_dim(instance, mining_dim_path):
    mining_dim_folder = os.path.join(instance, mining_dim_path)
    if exists(mining_dim_folder):
        shutil.rmtree(mining_dim_folder)
        print(f"Completed: {mining_dim_path}")
    else:
        print(f"{mining_dim_path} does not exist")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Define mining dimension names and their paths
mining_dim_info = {
    "twilight_forest": "dimensions/twilight_forest",
    "dim1": "DIM1",
    # Add more mining dimensions as needed
}

# Initialize the AMP API connection
API = ADS("http://localhost:8080/", "admin", "myfancypassword123")
API.Login()

# Send a tellraw command to Minecraft players on a specific instance
def send_tellraw_command(instance_name, message):
    command = f"/tellraw @a {{\"text\":\"{message}\"}}"
    API.InstanceLogin(instance_name, "Minecraft").Core.SendConsoleCommand(command)

# Fetch the list of instances
instances = API.ADSModule.GetInstances()["result"]

# Create a dictionary to store the original running status of instances
original_running_instances = {instance["Name"]: instance["State"] for instance in instances}

# Stop all instances using the API
API.ADSModule.StopAllInstances()

# Calculate the time until shutdown (in seconds)
shutdown_time = 30 * 60  # 30 minutes

# Notify players of the upcoming shutdown at specific intervals
notify_times = [15 * 60, 5 * 60, 60, 10, 5]  # in seconds

# Iterate through each instance and send tellraw notifications
for instance in instances:
    instance_name = instance["Name"]
    send_tellraw_command(instance_name, f"Server {instance_name} will shut down in {shutdown_time // 60} minutes.")

# Start the countdown
for elapsed_time in range(shutdown_time, -1, -1):
    for instance in instances:
        instance_name = instance["Name"]
        if elapsed_time in notify_times:
            minutes, seconds = divmod(elapsed_time, 60)
            send_tellraw_command(instance_name, f"Server {instance_name} will shut down in {minutes} minutes and {seconds} seconds.")

    # Wait for 1 second before checking again
    time.sleep(1)

# Wait for all instances to shut down
shutdown_timeout = 180  # 3 minutes
start_time = time.time()

all_stopped = False  # Variable to track if all instances have stopped

while True:
    # Fetch the statuses of all instances
    instance_statuses = API.ADSModule.GetInstanceStatuses()["result"]

    # Check if all instances are stopped
    all_stopped = all(status["State"] == "Stopped" for status in instance_statuses)

    if all_stopped:
        break

    # Check if it has been 3 minutes
    elapsed_time = time.time() - start_time
    if elapsed_time > shutdown_timeout:
        # Send a kill command to instances that haven't shut down
        for status in instance_statuses:
            if status["State"] != "Stopped":
                print(f"Sending kill command to {status['Name']}...")
                API.Core.Kill(status["Name"])

    time.sleep(5)  # Wait for 5 seconds before checking again

# Reset code for each instance
for instance in instance_statuses:
    instance_name = instance["Name"]
    print(f"Processing instance: {instance_name}")

    # Reset code for each instance can be added here
    DragonReset.DragonReset(instance_name)

    # Reset mining dimensions and "DIM1"
    for mining_dim_name, mining_dim_path in mining_dim_info.items():
        reset_mining_dim(instance_name, mining_dim_path)

    print(f"Finished processing instance: {instance_name}\n")

# Start instances that were originally running
for instance_name, original_state in original_running_instances.items():
    if original_state == "Running" and instance_name not in [status["Name"] for status in instance_statuses]:
        print(f"Starting instance: {instance_name}")
        API.ADSModule.StartInstance(instance_name)

# Clear the screen
clear()
