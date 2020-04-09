from tkinter import *
from tkinter import ttk
import requests
import subprocess


class ControlApp:

    def __init__(self, master):

        # Main Window
        self.master = master
        self.master.geometry("900x700+200+200")
        self.master.title("Pi Controller (BETA)")
        self.master.iconbitmap(r'assets\images\favicon.ico')

        # Panels
        self.control_panel = ttk.Frame(master)
        self.command_panel = ttk.Frame(master)
        self.list_panel = ttk.LabelFrame(master, text="Discovered PIs")

        self.control_panel.config(height=100, width=300, relief=RIDGE)
        self.list_panel.config(height=500, width=500, relief=RIDGE)
        self.command_panel.config(height=300, width=500, relief=GROOVE)

        self.control_panel.grid(row=0, column=0, stick='nesw')
        self.list_panel.grid(row=0, column=1, stick='nesw', pady=5, padx=5)
        self.command_panel.grid(row=1, column=0, columnspan=2, stick='nesw', pady=10)

        # Menu
        self.menu_bar = Menu(master)
        self.master.config(menu=self.menu_bar)
        self.file = Menu(self.menu_bar)
        self.edit = Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.file, label="File")
        self.menu_bar.add_cascade(menu=self.edit, label="Edit")

        self.file.add_command(label="New", command=lambda: print("test"))


        # Command Panel Widgets
        self.command_input = ttk.Entry(self.command_panel, width=100)
        self.command_input.grid(row=0, column=0, sticky='w')

        self.command_response = Text(self.command_panel)
        self.command_response.config(height=10, width=110)
        self.command_response.grid(row=1, column=0)

        self.response_scroll = ttk.Scrollbar(self.command_panel, orient=VERTICAL, command=self.command_response.yview)
        self.response_scroll.grid(row=1, column=1, stick='ns')
        self.command_response.config(yscrollcommand=self.response_scroll.set)

        # List Panel Widgets
        self.list_box = Listbox(self.list_panel, height=20, width=80)
        self.list_box.grid(row=0, column=0)

        self.scrollbar = ttk.Scrollbar(self.list_panel, orient=VERTICAL, command=self.list_box.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.list_box.config(yscrollcommand=self.scrollbar.set)

        self.list_box.bind("<Double-Button-1>", self.on_double)

        # Control Panel Widgets
        # TODO: Work On Control Panel Widgets

        for _ in range(30):
            self.list_box.insert("end", f"192.168.1.{_}")

    def on_double(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        print(value)
        spawn = SSH(value)
        spawn.start()


class SSH:

    def __init__(self, ip_address="", username="pi", password="raspberry"):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        # See if putty exists. If not, download it.
        try:
            self.file = open("putty.exe")
            self.file.close()
        except FileNotFoundError:
            self.download_putty()

    @staticmethod
    def download_putty():
        """
        This method is only called if putty is not detected
        :return:
        """
        file_url = "https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe"
        download_file = requests.get(file_url, stream=True)

        with open("putty.exe", "wb") as putty:
            for chunk in download_file.iter_content(chunk_size=1024):
                if chunk:
                    putty.write(chunk)

    def start(self):
        try:
            subprocess.Popen(f"putty.exe {self.username}@{self.ip_address} -pw {self.password}")
        except Exception as e:
            print(e)






def main():
    root = Tk()
    app = ControlApp(root)
    root.mainloop()

if __name__ == '__main__': main()


