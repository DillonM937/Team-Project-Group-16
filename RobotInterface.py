import tkinter as tk

window = tk.Tk()
window.geometry("590x300")  # Size of the window 
window.title("Remote Control")  # Adding a title



strVar = tk.StringVar()
l1 = tk.Label(window,  textvariable=strVar, width=20, height = 10, bg = "light blue" ) #create label for display the button that clicked
l1.grid(row=0,column=0,columnspan=10, padx = 1, pady= 20, sticky = 'ew') 


def show_work(pressed_btn):  #function to set the button to strVar for display on label
    strVar.set(pressed_btn)

robot_func = ("Start","Stop","Dump Container","Pause")
count = 0

#loop to create and assign button
for work in robot_func:
    btn = tk.Button(window, text=work, height = 2, width = 15, command=lambda lan=work:show_work(lan))
    btn.grid(row=1,column=count, padx = 15, pady= 15, sticky='ew')
    count += 1

window.mainloop()


