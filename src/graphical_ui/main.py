from tkinter import *

# Creating an instance of the frame:
root = Tk()

# Simple text in gui:
"""
my_label_1 = Label(root, text="Hello there!")
my_label_2 = Label(root, text="A great gui application!")

my_label_1.grid(row=0, column=0)
my_label_2.grid(row=1, column=1)
"""


# Buttons:
"""
# Enabled button:
my_button_e = Button(root, text="Click Me!")

# Disable Button:
my_button_d = Button(root, text="Try clicking!", state=DISABLED)

# Changing the size of the button:
my_button_c_x = Button(root, text="(Wider on X-axis) Click me!", padx=100)
my_button_c_y = Button(root, text="(Wider on Y-axis) Click me!", pady=100)

my_button_c_xy = Button(root, text="(Wider on both axes) Click me!", padx=120, pady=120)

my_button_e.grid(row=0, column=0)
my_button_d.grid(row=0, column=1)
my_button_c_x.grid(row=0, column=2)
my_button_c_y.grid(row=0, column=3)
my_button_c_xy.grid(row=0, column=4)


# Showing a message after a button was clicked:
def clicked():
    after_click = Label(root, text="I was clicked!")
    after_click.grid()


my_button_click = Button(root, text="Click me for a surprise!", command=clicked)
my_button_click.grid(row=1, column=2)


# Changing the color of the text of the button (hex can be used):
my_button_fg_color = Button(root, text="Colorful me! Definitely click!", fg="green")
my_button_fg_color.pack()

# Changing the color of the background of the button (hex can be used):
my_button_bg_color = Button(root, text="Colorful me! Different variant!", bg="green")
my_button_bg_color.pack()
"""

# Entry widget:
"""
entry = Entry(root)
entry.pack()

# Changing the size of the entry widget:
entry_s = Entry(root, width=30)
entry_s.pack()

# Changing the color of the text put in the entry:
entry_fg_color = Entry(root, fg="red")
entry_fg_color.pack()

# Changing the color of the background of the entry:
entry_bg_color = Entry(root, bg="yellow")
entry_bg_color.pack()

# Changing the border width of the entry:
entry_bw = Entry(root, borderwidth=6)
entry_bw.pack()
"""


# Getting the input entered:
name = Label(root, text="Enter your name: ")
name_entry = Entry(root, width=20)


def show_name():
    show = Label(root, text=f"Hello {name_entry.get()}!")
    show.grid(column=1)


entered_name = Button(root, text="Your Name: ", command=show_name)

name.grid()
name_entry.grid(row=0, column=1)
entered_name.grid(row=1, column=0)

root.mainloop()
