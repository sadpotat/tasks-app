# Default path
import os
import json
from shutil import copy

APP_DIR = os.path.expanduser("~\\Documents\\Tasker")
CONFIG_PATH = os.path.join(APP_DIR, "config.json")


def create_config(app_dir=APP_DIR, config_path=CONFIG_PATH):
    """ This method creates the config file at config_path. """
    # Create dictionaries to store paths
    default_paths = {
        "today": os.path.join(app_dir, "Today.txt"),
        "repeat": os.path.join(app_dir, "Everyday.txt"),
        "general": os.path.join(app_dir, "General.txt")}

    last_loaded = {
        "today": None,
        "repeat": None,
        "general": None}

    # write file
    with open(config_path, "w") as outfile:
        # Write the data to the file in JSON format
        json.dump([default_paths, last_loaded], outfile)


def get_config(app_dir=APP_DIR, config_path=CONFIG_PATH):
    """ This method checks if the config file exists 
    and returns its path. """
    # Create the config file if it doesn't exist
    if not os.path.exists(config_path):
        create_config(app_dir, config_path)
    return config_path


def create_defaults(defaults):
    """ This method creates the default profiles. """
    for path in defaults.values():
        if not os.path.exists(path):
            open(path, 'a').close()


def get_defaults(app_dir=APP_DIR, config_path=CONFIG_PATH):
    """ This method returns the path to the default profiles. """
    # Load the JSON data from the file
    with open(config_path, 'r') as file:
        data = json.load(file)
    defaults = data[0]
    create_defaults(defaults)
    return defaults


def check_temp(config_path=CONFIG_PATH):
    """ This method creates the Temp directory if it does not exist. """
    temp_path = os.path.dirname(config_path) + "//Temp"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    return temp_path


def get_last_loaded_files(config_path=CONFIG_PATH):
    """ This method gets the last_loaded dict from config_path. """
    with open(config_path, 'r') as file:
        data = json.load(file)
    return data[1]


def write_to_config(data, config_path=CONFIG_PATH):
    """ This method updates the config file. """
    with open(config_path, "w") as outfile:
        json.dump(data, outfile)


def load_from_file(filepath):
    """ This method loads the list in filepath. """
    with open(filepath, 'r') as file_load:
        return file_load.readlines()


def write_to_file(task_list, filepath):
    """writes task_list to filepath."""
    with open(filepath, 'w') as file:
        file.writelines(task_list)


def add_to_list(task_list, new_task, filepath):
    """ This method adds a new item to task_list and
        then writes the list to filepath. """
    try:
        task_list.append(new_task)
        write_to_file(task_list, filepath)
        return task_list
    except:
        return load_from_file(filepath)


def edit_task(task_list, index, edited_task, filepath):
    """ This method assigns edited_task to task_list[index]
        and then writes the list to filepath. """
    try:
        task_list[index] = edited_task
        write_to_file(task_list, filepath)
        return task_list
    except:
        return load_from_file(filepath)


def remove_task(task_list, completed_task, filepath):
    """ This method deletes task_list[index] and 
        writes the list to filepath. """
    try:
        task_list.remove(completed_task)
        write_to_file(task_list, filepath)
        return task_list
    except:
        return load_from_file(filepath)


if __name__ == '__main__':
    pass
