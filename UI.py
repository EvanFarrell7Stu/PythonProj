import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("BER Ireland")
root.geometry("500x300")  # Width x Height

# Create a label widget
label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
label.pack(pady=10)

# Create an entry widget
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Define what happens when the button is clicked
def greet_user():
    name = name_entry.get()
    if name.strip() == "":
        messagebox.showwarning("Input Error", "Please enter your name.")
    else:
        messagebox.showinfo("Greeting", f"Hello, {name}!")

# Create a button widget
greet_button = tk.Button(root, text="Greet Me", command=greet_user, font=("Arial", 10), bg="#4CAF50", fg="white")
greet_button.pack(pady=10)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10), bg="#f44336", fg="white")
exit_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
