from datetime import date
import os

x = date.today()
print(x)

my_docs_path = os.path.expanduser("~\\Documents\\Tasker")

# Create the directory path if it doesn't already exist
if not os.path.exists(my_docs_path):
    os.makedirs(my_docs_path)

# Create a text file in the My Documents folder
file_path = os.path.join(my_docs_path, "congig.txt")
with open(file_path, "w") as f:
    f.write("Hello, world!")
