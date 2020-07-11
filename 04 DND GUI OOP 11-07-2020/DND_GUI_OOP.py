import tkinter as tk
#import screenconfigs as sc

window = tk.Tk()

main_screen = tk.Button(
    text="Click to start",
    fg="white",
    activeforeground="white",
    bg="black",
    activebackground="black",
    width=100,
    height=20
)

main_screen.pack()

window.mainloop()