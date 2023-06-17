import os
from datetime import datetime, date
from shutil import copy
import PySimpleGUI as gui
import functions as m
print(date.today())

def load_variables(FILE_NAME, fname, window_key):
    FILE_NAME = temp_path + "//" + \
        os.path.basename(FILE_NAME)
    copy(fname, FILE_NAME)
    task_list = m.load_from_file(FILE_NAME)
    window[window_key].update(
        values=task_list)
    return [FILE_NAME, task_list]


# Initialization
gui.theme("LightGreen7")
gui.set_options(element_padding=(0, 0))
font = ("Helvetica", 12)
button_size = [4, 1]
im_size = (24, 24)
ADD_ICON = r"icons\add.png"
EDIT_ICON = r"icons\edit.png"
COMPLETE_ICON = r"icons\done.png"
DELETE_ICON = r"icons\delete.png"
SAVE_ICON = r"icons\save.png"
config_path = m.get_config()
default_dict = m.get_defaults()
loaded_dict = m.get_last_loaded_files()
temp_path = m.check_temp()

# default filepaths are in default_dict
FILE_TODAY = default_dict["today"]
FILE_REP = default_dict["repeat"]
FILE_GEN = default_dict["general"]

# loaded files
for key, value in loaded_dict.items():
    if value is None:
        loaded_dict[key] = default_dict[key]

last_saved = None

# Getting modification dates as datetime objects for daily and repeating tasks
mod_date = []
for file in [FILE_TODAY, FILE_REP]:
    # Get the modification time of the file in seconds since the epoch
    modification_time = os.path.getmtime(file)

    # Convert the modification time into a datetime object
    modification_date = datetime.fromtimestamp(modification_time).date()

    mod_date.append(modification_date)

# delete daily tasks if today's date doesn't match last modified date
if not mod_date[0] == date.today():
    m.write_to_file([], FILE_TODAY)
print(mod_date)
# if the temp file for repeating tasks exists and it was created the same day, FILE_REP = <path to temp file>
# else deletes the temp file so that repeating tasks reload
rep_temp_path = temp_path + f"//{os.path.basename(FILE_REP)}"
if os.path.exists(rep_temp_path) and mod_date[1]!=date.today():
    os.remove(rep_temp_path)
if not os.path.exists(rep_temp_path):
    copy(FILE_REP, rep_temp_path)
FILE_REP = rep_temp_path


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
delete_button = gui.Button(
    key="Delete", image_source=DELETE_ICON, size=1, tooltip=" Delete task ")
save_button = gui.Button(
    key="Save", image_source=SAVE_ICON, size=1, tooltip=" Save to profile ")
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
           gui.Column([[add_button], [edit_button], [complete_button], [delete_button],
                       [gui.T("", size=[1, 3])], [save_button]])],
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
            if fname is not None:
                if not fname.endswith(".txt"):
                    gui.popup(
                        "Loading Aborted: File format is not supported", font=font)
                    continue
                if fname != "":
                    fname = os.path.normpath(fname)
                    if event == "Today's Tasks":
                        # copies loaded profile to a temporary file
                        loaded_dict["today"] = fname
                        FILE_TODAY, task_list = load_variables(
                            FILE_TODAY, fname, "task_list_today")
                        filename = FILE_TODAY
                    elif event == "Repeating Tasks":
                        loaded_dict["repeat"] = fname
                        # checks if fname has a temp file. If the file was modified the same day, load that file else rewrite temp file
                        rep_temp_path = temp_path + f"//{os.path.basename(fname)}"
                        if os.path.exists(rep_temp_path):
                            mod_time = os.path.getmtime(rep_temp_path)
                            mod_date[1] = datetime.fromtimestamp(mod_time).date()
                            if mod_date[1]==date.today():
                                FILE_REP = rep_temp_path
                                task_list = m.load_from_file(FILE_REP)
                                window["task_list_rep"].update(
                                    values=task_list)
                            else:
                                os.remove(rep_temp_path)
                        if not os.path.exists(rep_temp_path):
                            FILE_REP, task_list = load_variables(FILE_REP, fname, "task_list_rep")
                        filename = FILE_REP
                    else:
                        loaded_dict["general"] = fname
                        FILE_GEN, task_list = load_variables(
                            FILE_GEN, fname, "task_list_gen")
                        filename = FILE_GEN
                    m.write_to_config([default_dict, loaded_dict])

        case "tabs":
            # reloads the task_list and filename variable everytime you switch tabs
            
            if values["tabs"] == "tab1":
                # delete daily tasks if today's date doesn't match last modified date, repeated again in case the application is left running
                if not mod_date[0] == date.today():
                    m.write_to_file([], FILE_TODAY)
                filename = FILE_TODAY
                loaded_key = "today"
                value_task = "task_today"
                value_tasklist = "task_list_today"
                if FILE_TODAY == last_saved:
                    task_list = m.load_from_file(filename)
                    window[f"{value_tasklist}"].update(values=task_list)
            
            elif values["tabs"] == "tab2":
                # if the temp file for repeating tasks exists and it was created the same day, FILE_REP = <path to temp file>
                # else deletes the temp file so that repeating tasks reload
                rep_temp_path = temp_path + f"//{os.path.basename(FILE_REP)}"
                # mod_time = os.path.getmtime(rep_temp_path)
                # mod_date[1] = datetime.fromtimestamp(mod_time).date()
                if os.path.exists(rep_temp_path) and mod_date[1]!=date.today():
                    os.remove(rep_temp_path)
                if not os.path.exists(rep_temp_path):
                    copy(loaded_dict["repeat"], rep_temp_path)
                FILE_REP = rep_temp_path
                
                filename = FILE_REP
                loaded_key = "repeat"
                value_task = "task_rep"
                value_tasklist = "task_list_rep"
                if FILE_REP == last_saved:
                    task_list = m.load_from_file(filename)
                    window[f"{value_tasklist}"].update(values=task_list)

            else:
                filename = FILE_GEN
                loaded_key = "general"
                value_task = "task_gen"
                value_tasklist = "task_list_gen"
                if FILE_GEN == last_saved:
                    task_list = m.load_from_file(filename)
                    window[f"{value_tasklist}"].update(values=task_list)
            task_list = m.load_from_file(filename)

        case "Add":
            # rejects whitespaces in input string
            new_task = values[f"{value_task}"].strip()
            if new_task == "":
                gui.popup("Please type a task first!",
                          font=font, no_titlebar=False)
                continue
            new_task = new_task[0].upper() + new_task[1:] + '\n'
            # rejects duplicates
            if new_task in task_list:
                gui.popup("Task already exists!", font=font)
                continue
            task_list = m.add_to_list(task_list, new_task, filepath=filename)

            if values["tabs"] == "tab2":
                m.add_repeating_task(new_task, loaded_dict["repeat"])

            # updates the listbox widget
            window[f"{value_tasklist}"].update(values=task_list)

        case "task_list_today" | "task_list_rep" | "task_list_gen":
            # workaround for IndexErrors
            if values[f"{value_tasklist}"] == []:
                continue
            window[f"{value_task}"].update(
                value=values[f"{value_tasklist}"][0].strip())

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
            edited_task = edited_task[0].upper() + edited_task[1:] + '\n'
            # rejects duplicates
            if edited_task in task_list:
                gui.popup("Task already exists!",
                          font=font)
                continue

            task_list = m.edit_task(task_list, task_list.index(values[f"{value_tasklist}"][0]),
                                    edited_task, filepath=filename)
            window[f"{value_tasklist}"].update(values=task_list)

            # also edits task in main profile
            if values["tabs"] == "tab2":
                task_temp = m.load_from_file(loaded_dict["repeat"])
                m.edit_task(task_temp, task_temp.index(values[f"{value_tasklist}"][0]),
                            edited_task, filepath=loaded_dict["repeat"])

        case 'Complete' | 'Delete':
            # rejects when you select empty space
            if values[f"{value_tasklist}"] == []:
                gui.popup("Please select a task first!",
                          font=font)
                continue

            # updates main repeating profile
            if event == "Delete" and values["tabs"] == "tab2":
                delete = gui.popup_ok_cancel(
                    "This will permanently remove the task", font=font)
                if delete == "OK":
                    m.remove_task(m.load_from_file(
                        loaded_dict["repeat"]), values[f"{value_tasklist}"][0], loaded_dict["repeat"])
                else:
                    continue

            task_list = m.remove_task(
                task_list, values[f"{value_tasklist}"][0], filepath=filename)
            window[f"{value_tasklist}"].update(values=task_list)
            window[f"{value_task}"].update(value="")

        case "Save":
            save_popup = gui.popup_ok_cancel(
                "This will overwrite the original file", font=font)
            if save_popup == "OK":
                m.write_to_file(task_list, loaded_dict[loaded_key])
                last_saved = loaded_dict[loaded_key]

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break

window.close()
