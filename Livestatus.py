import json
import threading
import time
import server_requests
import tkinter as tk
from tkinter import ttk


def get_url(server):
    return f"https://panel.simrail.eu:8084/stations-open?serverCode={server.lower()}"

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live Status")

        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        self.url = json.load(open('config.txt'))['url']
        self.servers = server_requests.get_server(self.url)

        self.listboxes = {}
        for server in self.servers:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=server['servercode'])
            self.listboxes[server['servercode']] = tk.Listbox(tab, width=50, height=20)
            self.listboxes[server['servercode']].grid(row=0, column=0)
        self.update_data()


    def update_data(self):
        for server in self.servers:
            print(server['servercode'])
            self.listboxes[server['servercode']].delete(0, tk.END)
            stations = server_requests.get_data(server['servercode'],self.url)
            for station in stations:
                print(station)
                if station['available']:
                    self.listboxes[server['servercode']].insert(
                        tk.END, f'\u2705 {station["name"]}')
                else:
                    self.listboxes[server['servercode']].insert(
                        tk.END, f'\u274C {station["name"]}')
        time.sleep(1)
        threading.Thread(target=self.update_data).start()





if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
