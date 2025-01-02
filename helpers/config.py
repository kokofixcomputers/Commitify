import configurationlib
import subprocess
import platform
import os

def init_config_files(branch, standard_format):
    current_dir = os.getcwd()
    config = configurationlib.Instance(file=os.path.join(current_dir, ".commitify", "config.json"), format=configurationlib.Format.JSON)
    try:
        exists = config.get()['initiated']
        return
    except:
        config.save()['initiated'] = True
    config.save()['branch'] = str(branch)
    config.save()['format'] = str(standard_format)
    config.save()

def ensure_project_directory(dir, branch, standard_format):
    # Directory name for commitify config
    dir_name = ".commitify"

    if not os.path.isdir(os.path.join(dir, ".commitify")):
        return_boolean = False
        # Create the directory if does not exist
        os.makedirs(dir_name)

        if platform.system() == "Windows":
            # For Windows, use attrib command to set hidden attribute
            subprocess.run(["attrib", "+h", dir_name], shell=True)
        elif platform.system() == "Darwin":
            # For macOS, use chflags command to set hidden attribute
            subprocess.run(["chflags", "hidden", dir_name])
        elif platform.system() == "Linux":
            # For Linux, simply having a dot in front of the name makes it hidden
            pass
        init_config_files(branch, standard_format)
    else:
        return_boolean = True
    return return_boolean

def check_project_directory(dir):
    if not os.path.isdir(os.path.join(dir, ".commitify")):
        return False
    return True

