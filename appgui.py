import os
import methods as m
import PySimpleGUI as gui

# Initialization
gui.theme("LightGreen7")
gui.set_options(element_padding=(0, 0))
font = ("Helvetica", 12)
button_size = [4, 1]
im_size = (24, 24)
add_icon = r"icons\add.png"
edit_icon = r"icons\edit.png"
complete_icon = r"icons\done.png"
# default filepaths are in m.DATA_FILES
file_today = m.DATA_FILES[0]
file_rep = m.DATA_FILES[1]
file_gen = m.DATA_FILES[2]
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
add_button_today = gui.Button(
    key="Add_today", image_source=add_icon, size=1, tooltip=" Add task ")
edit_button_today = gui.Button(
    key="Edit_today", image_source=edit_icon, size=1, tooltip=" Edit task ")
complete_button_today = gui.Button(
    key="Complete_today", image_source=complete_icon, size=1, tooltip=" Complete task ")
listbox_today = gui.Listbox(values=m.load_from_file(file_today),
                            key="task_list_today", enable_events=True, size=[45, 10],
                            tooltip=" Current tasks ")

# widgets in Tab2
label_rep = gui.Text("Enter a task:")
inputbox_rep = gui.InputText(key="task_rep", size=[45, 1])
add_button_rep = gui.Button(
    key="Add_rep", image_source=add_icon, size=1, tooltip=" Add task ")
edit_button_rep = gui.Button(
    key="Edit_rep", image_source=edit_icon, size=1, tooltip=" Edit task ")
complete_button_rep = gui.Button(
    key="Complete_rep", image_source=complete_icon, size=1, tooltip=" Complete task ")
listbox_rep = gui.Listbox(values=m.load_from_file(file_rep),
                          key="task_list_rep", enable_events=True, size=[45, 10],
                          tooltip=" Current tasks ")
# widgets in Tab3
label_gen = gui.Text("Enter a task:")
inputbox_gen = gui.InputText(key="task_gen", size=[45, 1])
add_button_gen = gui.Button(
    key="Add_gen", image_source=add_icon, size=1, tooltip=" Add task ")
edit_button_gen = gui.Button(
    key="Edit_gen", image_source=edit_icon, size=1, tooltip=" Edit task ")
complete_button_gen = gui.Button(
    key="Complete_gen", image_source=complete_icon, size=1, tooltip=" Complete task ")
listbox_gen = gui.Listbox(values=m.load_from_file(file_gen),
                          key="task_list_gen", enable_events=True, size=[45, 10],
                          tooltip=" Current tasks ")

exit_button = gui.Button("Exit")
# will be deleted later
add_button = gui.Button(
    key="Add", image_source=add_icon, size=1, tooltip=" Add task ")
edit_button = gui.Button(
    key="Edit", image_source=edit_icon, size=1, tooltip=" Edit task ")
complete_button = gui.Button(
    key="Complete", image_source=complete_icon, size=1, tooltip=" Complete task ")

label = gui.Text("Type in a to-do:")
inputbox = gui.InputText(tooltip="Enter a to-do here",
                         key="task", size=[45, 1])
listbox = gui.Listbox(values=m.load_from_file("data.txt"),
                      key="task_list", enable_events=True, size=[45, 10],
                      tooltip=" Current tasks ")
# Layout takes a list of lists that contain the elements we want to place in the window.
# Each sublist in the superlist represents a row in the GUI
tab_today = [[label_today],
             [gui.Column([[inputbox_today], [listbox_today]]),
              gui.Column([[add_button_today], [edit_button_today], [complete_button_today]])]]
tab_repeating = [[label_rep],
                 [gui.Column([[inputbox_rep], [listbox_rep]]),
                  gui.Column([[add_button_rep], [edit_button_rep], [complete_button_rep]])]]
tab_general = [[label_gen],
               [gui.Column([[inputbox_gen], [listbox_gen]]),
                gui.Column([[add_button_gen], [edit_button_gen], [complete_button_gen]])]]
layout = [[gui.Menu(menu_def, font=font)],
          [gui.TabGroup([[gui.Tab("Today", tab_today, key="tab1")],
                         [gui.Tab("Repeating", tab_repeating, key="tab2")],
                         [gui.Tab("General", tab_general, key="tab3")]], key="tabs")],
          [label],
          [gui.vtop([gui.Column([[inputbox], [listbox], [exit_button]]),
                     gui.Column([[add_button], [edit_button], [complete_button]])])]]

# places widgets on a window object
window = gui.Window('Tasks', layout=layout, font=font)
# loads data from m.DATA_FILE by default
task_list = m.load_from_file("data.txt")

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
                filename = fname
                task_list = m.load_from_file(filepath=filename)
                window["task_list"].update(values=task_list)

        case "Add":
            # rejects whitespaces in input string
            new_task = values["task"].strip()
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
            window["task_list"].update(values=task_list)

        case "task_list":
            # workaround for IndexErrors
            if values["task_list"] == []:
                continue
            window["task"].update(value=values["task_list"][0])

        case "Edit":
            # rejects when you select empty space in listbox
            if values["task_list"] == []:
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
            if edited_task in task_list:
                gui.popup("Task already exists!",
                          font=font)
                continue

            task_list = m.edit_task(task_list, task_list.index(values["task_list"][0]),
                                    edited_task, filepath=filename)
            window["task_list"].update(values=task_list)

        case 'Complete':
            # rejects when you select empty space
            if values["task_list"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue
            task_list = m.remove_task(
                task_list, values["task_list"][0], filepath=filename)
            window["task_list"].update(values=task_list)
            window["task"].update(value="")

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break

window.close()
