from datetime import datetime, timedelta
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno
from ctypes import windll
from PIL import ImageTk, Image
import variables

#no blur
windll.shcore.SetProcessDpiAwareness(1)

#shorten
now = datetime.now()
toaster = ToastNotifier()


# -- tkinter tings --
class App(tk.Tk):

    def __init__(self):

        super().__init__()

        #get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        #scalable window dimensions
        window_width = int(screen_width/1.5)
        window_height = int(screen_height/1.5)

        #center the window
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        #set window size
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

        #hide titlebar
        self.overrideredirect(True)

        #fake titlebar
        title_bar = Frame(self)
        title_bar.pack()

        #icon
        icon_img_size = (25, 25)
        icon_img = Image.open(variables.icon)
        icon_img = icon_img.resize(icon_img_size)
        icon_img = ImageTk.PhotoImage(icon_img)

        icon_label = tk.Label(title_bar, image = icon_img)
        icon_label.grid(column=0, row=0, padx=0, pady=0)
        icon_label.image = icon_img

        #title (srsly need bhetter code fo r this, if u just change font then u mess up entirte titlebar)
        title_label = tk.Label(title_bar, bg="red", text=variables.app_name, font=variables.font, width=int(window_width/9.5))
        title_label.grid(column=1, row=0, padx=0, pady=0)

        #make titlebar moveable
        def move_app(i):
            self.geometry(f"+{i.x_root}+{i.y_root}")

        title_label.bind("<B1-Motion>", move_app)

        #minimise button
        taskbar_button = False
        def minimise_window():
            if taskbar_button == False:
                self.wm_state('iconic')
            else:
                self.iconify()

        #close button
        close_img = Image.open(r".\visual\close_button.png")
        close_img   = close_img.resize((15, 15))
        close_img = ImageTk.PhotoImage(close_img)

        close1_img = Image.open(r".\visual\close_button1.png")
        close1_img = close1_img.resize((15, 15))
        close1_img = ImageTk.PhotoImage(close1_img)

        #confirmation
        def close_confirm():
            if taskbar_button == False:
                answer = askyesno(title='Confirmation',
                    message='Are you sure that you want to quit?')
                if answer:
                    self.destroy()
            else:
                pass

        close_button = tk.Button(title_bar, image = close_img, borderwidth=0, command=close_confirm, height=25, width=35)
        close_button.grid(column=2, row=0, padx=0, pady=0)

        #hover over = change colour
        def on_enter(i):
            close_button.config(bg = 'red')
            close_button.config(image = close1_img)

        def on_leave(i):
            close_button.config(bg = 'SystemButtonFace')
            close_button.config(image = close_img)

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        #tk vars
        ws_var=tk.StringVar()
        b_s_var=tk.StringVar()
        b_e_var=tk.StringVar()

        #labels
        ws_msg = tk.Label(self, text="Websites to be blocked are:")
        ws_msg.pack()
        b_s = tk.Label(self, text="Block starts at")
        b_s.pack()
        b_e = tk.Label(self, text="Block ends at:")
        b_e.pack()

        #entries
        ws_entry=tk.Entry(self, textvariable = ws_var,
            font = (variables.font,10,'normal'))
        ws_entry.pack()

        b_s_entry=tk.Entry(self, textvariable = b_s_var,
            font = (variables.font,10,'normal'))
        b_s_entry.pack()

        b_e_entry=tk.Entry(self, textvariable = b_e_var,
            font = (variables.font,10,'normal'))
        b_e_entry.pack()

        def save():
            websites=ws_var.get()
            websites = websites.split(",")
            block_start=b_s_var.get()
            block_end=b_e_var.get()

            print(', '.join(websites))

        # save button
        save_btn=tk.Button(self, text = 'Save', command = save, bg=variables.green, borderwidth=0, fg="white")
        save_btn.pack()


#window dimensions



# -- time calculations --
current_time = now.strftime("%H:%M:%S")
day = now.strftime("%d")

#block timings
block_end = "19:00:00"
block_start = "21:00:00"

#output
print("Current time is", current_time)
print("Day:", day)

#time diff
tdelta1 =  datetime.strptime(block_end, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")
tdelta2 = datetime.strptime(block_start, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")


#toasties!
if int(day) < int(day) + 1 and current_time >= "21:00" or int(day) < int(day) + 1 and current_time < "19:00":
    # block toasts
    if len(variables.websites) > 1:
        toaster.show_toast(variables.app_name, f"Blocks on {', '.join(variables.websites)} started",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

    elif len(variables.websites) == 1:
        toaster.show_toast(variables.app_name, f"Block on {variables.websites} started",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

    else:
        toaster.show_toast(variables.app_name, f"Nothing is being blocked",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

elif current_time >= "19:00": # 7pm time for yt
    # unblock toasts
    if len(variables.websites) > 1:
        toaster.show_toast(variables.app_name, f"Blocks on {', '.join(variables.websites)} ended",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

    elif len(variables.websites) == 1:
        toaster.show_toast(variables.app_name, f"Block on {' '.join(variables.websites)} started",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

    else:
        toaster.show_toast(variables.app_name, f"Nothing is being blocked",
            icon_path=variables.icon, duration=variables.toast_d, threaded=True)

#run tkinter
if __name__ == "__main__":
    app = App()
    app.mainloop()
