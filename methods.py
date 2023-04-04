# from time import strftime
DATA_FILE = "data.txt"  # variables are defined at the beginning, in all caps


def get_from_file(filepath=DATA_FILE):
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
    new_task = new_task + '\n'
    todo_list.append(new_task)
    write_to_file(todo_list, filepath)
    return todo_list


def edit_task(todo_list, index, edited_task, filepath=DATA_FILE):
    """ This method assigns edited_task to todo_list[index]
        and then writes the list to filepath. """
    try:
        todo_list[index] = edited_task + '\n'
        write_to_file(todo_list, filepath)
        return todo_list
    except:
        pass


'''
def remove_task(todo_list, index, filepath=DATA_FILE):
    if len(todo_list) < 1:
        print("The list has no items")

    index = prompt[7:].split(" ")
    try:
        for ind, i in enumerate(index):
            to_be_removed = to_do[int(i)-ind].strip()
            del to_do[int(i)-ind]
            print(to_be_removed.capitalize(), "has been removed")
    except:
        print("Please enter a valid index!")
    write_to_file(todo_list, filepath)


print(strftime("Today is %A, %B %d, %Y."))
print(strftime("It is now %I:%M:%S %p."))

'''

if __name__ == '__main__':
    print("practising modules")
