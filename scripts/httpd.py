# Script to start a HTTP server on port 8000
# For python3 only.

from os import system, chdir
from sys import executable

# Try to move to the root directory.

try:
    chdir('/')
except:
    pass

# Generate the command to start the server.

command = executable + ' -m http.server 8000'

# Run the command.

system(command)
