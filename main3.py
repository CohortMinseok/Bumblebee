import tkinter as tk

def say_hello():
    label.config(text="Hello, Tkinter!")

# Create the main window
root = tk.Tk()
root.title("Tkinter Hello World")

# Create a label widget
label = tk.Label(root, text="Welcome to Tkinter!")

# Pack the label into the main window
label.pack(padx=20, pady=20)

# Create a button widget
button = tk.Button(root, text="Say Hello", command=say_hello)

# Pack the button into the main window
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
