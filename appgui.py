import time
import os
import methods as m
import PySimpleGUI as gui

# Initialization
gui.theme("LightGreen7")
font = ("Helvetica", 12)
button_size = [4, 1]
im_size = (24, 24)
add_icon = r"icons\add.png"
edit_icon = r"icons\edit.png"
complete_icon = r"icons\done.png"
# file where user data is saved
filename = m.DATA_FILE
# creates the file if it doesn't exist
if not os.path.exists(filename):
    open(filename, 'a').close()

# GUI widgets
# here, key is used to identify individual widgets
day = gui.Text("", key="day")
clock = gui.Text("", key="clock")
label = gui.Text("Type in a to-do:")
inputbox = gui.InputText(tooltip="Enter a to-do here",
                         key="task", size=[45, 1])
add_button = gui.Button(
    key="Add", image_source=add_icon, size=1, tooltip=" Add to-do ")
listbox = gui.Listbox(values=m.load_from_file(),
                      key="todo_list", enable_events=True, size=[45, 10],
                      tooltip=" Current tasks ")
edit_button = gui.Button(
    key="Edit", image_source=edit_icon, size=1, tooltip=" Edit to-do ")
complete_button = gui.Button(
    key="Mark\nCompleted", image_source=complete_icon, size=1, tooltip=" Complete to-do ")
exit_button = gui.Button("Exit")

# Layout takes a list of lists that contain the elements we want to place in the window.
# Each sublist in the superlist represents a row in the GUI
layout = [[day, gui.Push(), clock],
          [label],
          [gui.vtop([gui.Column([[inputbox], [listbox], [exit_button]]),
                     gui.Column([[add_button], [edit_button], [complete_button]])])]]

# places widgets on a window object
window = gui.Window('Tasks', layout=layout, font=font)
# loads data from m.DATA_FILE by default
todo_list = m.load_from_file()
# a flag for the initial prompt, shown only once in every boot
file_prompted = False

# GUI mainloop:
while True:
    # refreshes time
    event, values = window.read(timeout=999)
    window["clock"].update(value=time.strftime("%I:%M:%S %p"))
    window["day"].update(value=time.strftime("%A, %B %d, %Y"))
    # conditionals related to the Confirmation popup
    if not file_prompted:
        button = gui.popup_ok_cancel("Do you want to load a different file?",
                                     title="Confirmation", font=font)
        if button == 'OK':
            fname = gui.popup_get_file('File to load', font=font)
            # if you press Cancel instead of Browse, popup_get_file() returns None
            # if you enter an empty path, popup_get_file() returns an empty string
            if not fname.endswith(".txt"):
                gui.popup("Loading Aborted", font=font)
                continue
            if fname is not None and fname != "":
                filename = fname
                todo_list = m.load_from_file(filepath=filename)
                window["todo_list"].update(values=todo_list)
            file_prompted = True
            continue
        else:
            file_prompted = True
            continue
    match event:
        case "Add":
            # rejects whitespaces in input string
            new_task = values["task"].strip()
            if new_task == "":
                gui.popup("Please type a task first!",
                          font=font, no_titlebar=False)
                continue
            new_task = new_task.capitalize() + '\n'
            # rejects duplicates
            if new_task in todo_list:
                gui.popup("Task already exists!", font=font)
                continue
            todo_list = m.add_to_list(todo_list, new_task, filepath=filename)
            # updates the listbox widget
            window["todo_list"].update(values=todo_list)

        case "todo_list":
            # workaround for IndexErrors
            if values["todo_list"] == []:
                continue
            window["task"].update(value=values["todo_list"][0])

        case "Edit":
            # rejects when you select empty space in listbox
            if values["todo_list"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue
            edited_task = values["task"].strip()
            # rejects whitespace edits
            if edited_task == "":
                gui.popup("Please type a task first!",
                          font=font)
                continue
            edited_task = edited_task.capitalize() + '\n'
            # rejects duplicates
            if edited_task in todo_list:
                gui.popup("Task already exists!",
                          font=font)
                continue

            todo_list = m.edit_task(todo_list, todo_list.index(values["todo_list"][0]),
                                    edited_task, filepath=filename)
            window["todo_list"].update(values=todo_list)

        case 'Mark\nCompleted':
            # rejects when you select empty space
            if values["todo_list"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue
            todo_list = m.remove_task(
                todo_list, values["todo_list"][0], filepath=filename)
            window["todo_list"].update(values=todo_list)
            window["task"].update(value="")

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break

window.close()
