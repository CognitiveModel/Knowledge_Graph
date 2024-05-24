import subprocess

# Define the command to run
command = "neo4j-admin server console"

# Run the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Get the output and error (if any)
output, error = process.communicate()

# Print the output and error
print("Output:", output.decode())
print("Error:", error.decode())


# from fabric import Config, Connection
# from fabric.tasks import execute
# from fabfile import start_neo4j

# # Establish connection
# conn = Connection('your_host')

# # Execute the command
# execute(start_neo4j, conn)