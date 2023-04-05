import PySimpleGUI as gui
import methods as m

label = gui.Text("Type in a to-do")
# key is the key of the dictionary containing inputtext that is returned in the event variable
inputbox = gui.InputText(tooltip="Enter a to-do", key="task")
add_button = gui.Button("Add")
listbox = gui.Listbox(values=m.get_from_file(),
                      key="todo_list", enable_events=True, size=[45, 10])
edit_button = gui.Button("Edit", size=[4, 1])
complete_button = gui.Button("Mark\nCompleted", size=[9, 2])
exit_button = gui.Button("Exit", size=[4, 1])


# Layout takes a list of lists that contain the elements we want to place in the window.
# Each list in the superlist represents a row in the gui so even if your gui only has one row,
# make sure to put items in a sublist. For example, layout = [[item_1, item_2, item_3]].
# To place elements in separate rows, make sure to place them in separate sublists.
# For example, layout = [[first_row_item_1, item_2],[second_row_item_1, item_2]]
window = gui.Window(
    'Tasks', layout=[[label], [inputbox, add_button], [listbox, edit_button, complete_button], [exit_button]],
    font=("Helvetica", 16))

todo_list = m.get_from_file()

while True:
    event, values = window.read()
    match event:

        case "Add":
            new_task = values["task"].strip()
            if new_task == "":  # rejects whitespaces
                gui.popup("Please type a task first!", font=(
                    "Helvetica", 16), no_titlebar=False)
                continue
            new_task = new_task.capitalize() + '\n'
            if new_task in todo_list:
                gui.popup("Task already exists", font=("Helvetica", 16))
                continue
            todo_list = m.add_to_list(todo_list, new_task)
            # window["key of the element we want to update"]
            window["todo_list"].update(values=todo_list)

        case "todo_list":
            if values["todo_list"] == []:
                continue
            window["task"].update(value=values["todo_list"][0])

        case "Edit":
            while True:
                if values["todo_list"] == []:
                    gui.popup("Please select a task first!",
                              font=("Helvetica", 16))
                    continue
                edited_task = values["task"].strip()
                if edited_task == "":
                    gui.popup("Please type a task first!",
                              font=("Helvetica", 16))
                    continue
                edited_task = edited_task.capitalize() + '\n'
                if edited_task in todo_list:
                    gui.popup("Task already exists",
                              font=("Helvetica", 16))
                    continue
                break
            # values["todo_list"] is a list,  values["todo_list"][0] is a string
            todo_list = m.edit_task(todo_list, todo_list.index(values["todo_list"][0]),
                                    edited_task)
            window["todo_list"].update(values=todo_list)

        case 'Mark\nCompleted':
            if values["todo_list"] == []:
                gui.popup("Please select a task first!",
                          font=("Helvetica", 16))
                continue
            todo_list = m.remove_task(
                todo_list, values["todo_list"][0])
            window["todo_list"].update(values=todo_list)
            window["task"].update(value="")

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break
window.close()
