from time import strftime

print(strftime("Today is %A, %B %d, %Y."))
print(strftime("It is now %I:%M:%S %p."))

data_file = "data.txt"
with open(data_file, 'r') as file_load:
    to_do = file_load.readlines()


def write_to_file(todo_list, filepath=data_file):
    """writes todo_list to filepath."""
    with open(filepath, 'w') as file:
        file.writelines(todo_list)


while True:
    prompt = input("Enter add, show, edit, remove or exit: ")

    if prompt.startswith("add"):
        try:
            # throws exception if there are whitespaces after add
            prompttest = prompt[2:].strip()
            if prompttest[1] == 't':
                pass
        except:
            print("Please enter a task!")
            continue
        new_item = prompt[4:] + '\n'
        to_do.append(new_item)
        write_to_file(to_do)

    elif prompt.startswith("show"):
        if len(to_do) < 1:
            print("The list is empty!")
            continue
        for index, item in enumerate(to_do):
            print(index, item.strip().capitalize())

    elif prompt.startswith("edit"):
        index = prompt[5:]
        try:
            new_item = input("Enter edited task: ")
            to_do[int(index)] = new_item + '\n'
            write_to_file(to_do)
        except:
            print("Please enter a valid index!")

    elif prompt.startswith("remove"):
        if len(to_do) < 1:
            print("The list has no items")
            continue
        index = prompt[7:].split(" ")
        try:
            for ind, i in enumerate(index):
                to_be_removed = to_do[int(i)-ind].strip()
                del to_do[int(i)-ind]
                print(to_be_removed.capitalize(), "has been removed")
        except:
            print("Please enter a valid index!")
        write_to_file(to_do)

    elif prompt.startswith("exit"):
        write_to_file(to_do)
        break

    else:
        print("Please enter a valid command!")
        continue
