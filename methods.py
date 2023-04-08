# Default path
DATA_FILES = ["Today.txt", "Everyday.txt", "General.txt"]


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
