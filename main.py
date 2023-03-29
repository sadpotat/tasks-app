data_file = "data.txt"
with open(data_file, 'r') as file_load:
    to_do = file_load.readlines()

while True:
    prompt = input("Enter add, show, edit, remove or exit: ")
    match prompt.strip():
        case "add":
            new_item = input("Enter a new task: ") + "\n"
            to_do.append(new_item)
        case "show":
            if len(to_do) < 1:
                print("The list is empty!")
                continue
            for item in to_do:
                print(item.strip().capitalize())
        case "edit":
            for i, item in enumerate(to_do):
                print(i, item.strip().capitalize())
            index = input("Enter the index of the item to be edited: ") + "\n"
            try:
                new_item = input("Enter edited task: ")
                to_do[int(index)] = new_item
            except:
                print("Please enter a valid index!")
        case "remove":
            if len(to_do) < 1:
                print("The list has no items")
                continue
            for i, item in enumerate(to_do):
                print(i, item.strip().capitalize())
            index = input("Enter the index of the item to be deleted: ")
            try:
                del to_do[int(index)]
            except:
                print("Please enter a valid index!")
        case "exit":
            with open(data_file, 'w') as file:
                file.writelines(to_do)
            break
        case _:
            print("Please enter a valid command!")
            continue
