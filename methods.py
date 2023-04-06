# Default path
DATA_FILE = "data.txt"


def load_from_file(filepath=DATA_FILE):
    """ This method loads the list in filepath. """
    with open(filepath, 'r') as file_load:
        return file_load.readlines()


def write_to_file(todo_list, filepath=DATA_FILE):
    """writes todo_list to filepath."""
    with open(filepath, 'w') as file:
        file.writelines(todo_list)


def add_to_list(todo_list, new_task, filepath=DATA_FILE):
    """ This method adds a new item to todo_list and
        then writes the list to filepath. """
    try:
        todo_list.append(new_task)
        write_to_file(todo_list, filepath)
        return todo_list
    except:
        return load_from_file()


def edit_task(todo_list, index, edited_task, filepath=DATA_FILE):
    """ This method assigns edited_task to todo_list[index]
        and then writes the list to filepath. """
    try:
        todo_list[index] = edited_task
        write_to_file(todo_list, filepath)
        return todo_list
    except:
        return load_from_file()


def remove_task(todo_list, completed_task, filepath=DATA_FILE):
    """ This method deletes todo_list[index] and 
        writes the list to filepath. """
    try:
        todo_list.remove(completed_task)
        write_to_file(todo_list, filepath)
        return todo_list
    except:
        return load_from_file()


if __name__ == '__main__':
    pass
