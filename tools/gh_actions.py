# THIS PYTHON FILE DOES NOT WORK WHEN EXECUTED ALONE. IT IS MEANT FOR GITHUB ACTIONS TO RUN THIS FILE.
import sys
import metadata

arg1 = sys.argv[1]  # First argument after the script name
arg2 = sys.argv[2]  # Second argument after the script name
arg3 = sys.argv[3]  # Third argument after the script name

if arg1 == "metadata":
    metadata.set_metadata("commitify.py", arg2, arg3)
