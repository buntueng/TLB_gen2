from tkinter import *
import pystray
from PIL import Image, ImageTk

# Create an instance of tkinter frame or window
win=Tk()

win.title("System Tray Application")
# Set the size of the window
win.geometry("700x350")

# Define a function for quit the window
def quit_window(icon,item):
   icon.stop()
   win.destroy()

# Define a function to show the window again
def show_window(icon,item):
   icon.stop()
   win.deiconify()

# Hide the window and show on the system taskbar
def hide_window():
   win.withdraw()
   image=Image.open("micons.png")
   tray_menu=(pystray.MenuItem('Quit', quit_window), pystray.MenuItem('Show', show_window))
   icon=pystray.Icon("name", image, menu=tray_menu)
   icon.run()

win.protocol('WM_DELETE_WINDOW', hide_window)

win.mainloop()