import os
import methods as m
import PySimpleGUI as gui

# Initialization
gui.theme("LightGreen7")
gui.set_options(element_padding=(0, 0))
font = ("Helvetica", 12)
button_size = [4, 1]
im_size = (24, 24)
ADD_ICON = r"icons\add.png"
EDIT_ICON = r"icons\edit.png"
COMPLETE_ICON = r"icons\done.png"
# default filepaths are in m.DATA_FILES
FILE_TODAY = m.DATA_FILES[0]
FILE_REP = m.DATA_FILES[1]
FILE_GEN = m.DATA_FILES[2]
# creates the files if they doesn't exist
for file in m.DATA_FILES:
    if not os.path.exists(file):
        open(file, 'a').close()

# Menu
menu_def = [["File", ["New", "Exit"]],
            ["Load", ["Today's Tasks", "Repeating Tasks", "General Tasks"]],
            ["Help", "About..."]]

# GUI widgets
# here, key is used to identify individual widgets
# widgets in Tab1
label_today = gui.Text("Enter a task:")
inputbox_today = gui.InputText(key="task_today", size=[45, 1])
listbox_today = gui.Listbox(values=m.load_from_file(FILE_TODAY),
                            key="task_list_today", enable_events=True, size=[45, 10],
                            tooltip=" Current tasks ")

# widgets in Tab2
label_rep = gui.Text("Enter a task:")
inputbox_rep = gui.InputText(key="task_rep", size=[45, 1])
listbox_rep = gui.Listbox(values=m.load_from_file(FILE_REP),
                          key="task_list_rep", enable_events=True, size=[45, 10],
                          tooltip=" Current tasks ")
# widgets in Tab3
label_gen = gui.Text("Enter a task:")
inputbox_gen = gui.InputText(key="task_gen", size=[45, 1])
listbox_gen = gui.Listbox(values=m.load_from_file(FILE_GEN),
                          key="task_list_gen", enable_events=True, size=[45, 10],
                          tooltip=" Current tasks ")

# buttons
add_button = gui.Button(
    key="Add", image_source=ADD_ICON, size=1, tooltip=" Add task ")
edit_button = gui.Button(
    key="Edit", image_source=EDIT_ICON, size=1, tooltip=" Edit task ")
complete_button = gui.Button(
    key="Complete", image_source=COMPLETE_ICON, size=1, tooltip=" Complete task ")
exit_button = gui.Button("Exit")

# Layout takes a list of lists that contain the elements we want to place in the window.
# Each sublist in the superlist represents a row in the GUI
tab_today = [[label_today],
             [gui.Column([[inputbox_today], [listbox_today]])]]
tab_repeating = [[label_rep],
                 [gui.Column([[inputbox_rep], [listbox_rep]])]]
tab_general = [[label_gen],
               [gui.Column([[inputbox_gen], [listbox_gen]])]]
layout = [[gui.Menu(menu_def, font=font)],
          [gui.TabGroup([[gui.Tab("Today", tab_today, key="tab1")],
                         [gui.Tab("Repeating", tab_repeating, key="tab2")],
                         [gui.Tab("General", tab_general, key="tab3")]], key="tabs", enable_events=True),
           gui.Column([[add_button], [edit_button], [complete_button]])],
          [exit_button]]

# places widgets on a window object
window = gui.Window('Tasks', layout=layout, font=font)
# loads data from m.DATA_FILE by default
task_list = m.load_from_file(FILE_TODAY)

# GUI mainloop:
while True:
    event, values = window.read()
    print(event)
    print(values)

    match event:
        case "Today's Tasks" | "Repeating Tasks" | "General Tasks":
            # load menu ->
            fname = gui.popup_get_file('File to load', font=font)
            # if you press Cancel instead of Browse, popup_get_file() returns None
            # if you enter an empty path, popup_get_file() returns an empty string
            if not fname.endswith(".txt"):
                gui.popup(
                    "Loading Aborted: File format is not supported", font=font)
                continue
            if fname is not None and fname != "":
                if event == "Today's Tasks":
                    FILE_TODAY = fname
                    window["task_list_today"].update(
                        values=m.load_from_file(FILE_TODAY))
                elif event == "Repeating Tasks":
                    FILE_REP = fname
                    window["task_list_rep"].update(
                        values=m.load_from_file(FILE_REP))
                else:
                    FILE_GEN = fname
                    window["task_list_gen"].update(
                        values=m.load_from_file(FILE_GEN))

        case "tabs":
            # reloads the task_list and filename variable everytime you switch tabs
            if values["tabs"] == "tab1":
                filename = FILE_TODAY
                value_task = "task_today"
                value_tasklist = "task_list_today"
            elif values["tabs"] == "tab2":
                filename = FILE_REP
                value_task = "task_rep"
                value_tasklist = "task_list_rep"
            else:
                filename = FILE_GEN
                value_task = "task_gen"
                value_tasklist = "task_list_gen"
            task_list = m.load_from_file(filename)

        case "Add":
            # rejects whitespaces in input string
            new_task = values[f"{value_task}"].strip()
            print(new_task)
            print(values[f"{value_task}"])
            print(f"{value_task}")
            if new_task == "":
                gui.popup("Please type a task first!",
                          font=font, no_titlebar=False)
                continue
            new_task = new_task.capitalize() + '\n'
            # rejects duplicates
            if new_task in task_list:
                gui.popup("Task already exists!", font=font)
                continue
            task_list = m.add_to_list(task_list, new_task, filepath=filename)
            # updates the listbox widget
            window[f"{value_tasklist}"].update(values=task_list)

        case "task_list_today" | "task_list_rep" | "task_list_gen":
            # workaround for IndexErrors
            if values[f"{value_tasklist}"] == []:
                continue
            window[f"{value_task}"].update(
                value=values[f"{value_tasklist}"][0])

        case "Edit":
            # rejects when you select empty space in listbox
            if values[f"{value_tasklist}"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue
            edited_task = values[f"{value_task}"].strip()
            # rejects whitespace edits
            if edited_task == "":
                gui.popup("Please type a task first!",
                          font=font)
                continue
            edited_task = edited_task.capitalize() + '\n'
            # rejects duplicates
            if edited_task in task_list:
                gui.popup("Task already exists!",
                          font=font)
                continue

            task_list = m.edit_task(task_list, task_list.index(values[f"{value_tasklist}"][0]),
                                    edited_task, filepath=filename)
            window[f"{value_tasklist}"].update(values=task_list)

        case 'Complete':
            # rejects when you select empty space
            if values[f"{value_tasklist}"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue
            task_list = m.remove_task(
                task_list, values[f"{value_tasklist}"][0], filepath=filename)
            window[f"{value_tasklist}"].update(values=task_list)
            window[f"{value_task}"].update(value="")

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break

window.close()
