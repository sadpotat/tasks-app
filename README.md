# tasks

 This is a small project. I started this because I needed a program to organise my work and I couldn't find one that did what I was looking for. 
 
 Implemented using the PySimpleGUI library.    
 <br />
 ![alt text](https://github.com/sadpotat/tasks-app/blob/main/screenshot.JPG?raw=true)
 <br />
 <br />
 ### Features:
 - Daily tasks: Will contain tasks for the day. These will be cleared everyday at 12:00 AM, no backup is kept.
 - Repeating tasks: Will reappear after a specific period of time.
 - General tasks: Nothing special. 
 - Profiles: A set of saved tasks that can be loaded into the program later.

 All data related to the program will be stored in `<user's home directory>\Documents\Tasker\`.  
 <br />
 <br />
 ### Things I haven't been able to implement yet:
 1. Dumping dailies at the start of the next day
 2. The whole repeating tasks function...
 3. Figuring out how to package icon images into the program's executable (I'm using PyInstaller).
