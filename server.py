import logging
import subprocess

# Define the command to run
# command = "neo4j-admin server console"
command = "neo4j start"

# Run the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Get the output and error (if any)
output, error = process.communicate()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log the output and error
logging.info("Output: %s", output.decode())
logging.error("Error: %s", error.decode())

# Check the return code
if process.returncode != 0:
    logging.error(f"Error: Command '{command}' failed with return code {process.returncode}")
