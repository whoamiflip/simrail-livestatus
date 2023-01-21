import json
import requests
import tkinter as tk
from tkinter import ttk


def get_url(server):
    return f"https://panel.simrail.eu:8084/stations-open?serverCode={server.lower()}"


def get_data(server):
    url = get_url(server)
    response = requests.get(url)
    json_data = json.loads(response.text)
    data = []
    for station in json_data['data']:
        station_obj = {
            'name': station['Name'],
            'available': len(station["DispatchedBy"]) == 0
        }
        data.append(station_obj)
    return data


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live Status")

        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        self.servers = ['DE1', 'DE2', 'DE3', 'DE4', 'DE5', 'EN1', 'EN2', 'EN3', 'EN4', 'EN5']

        self.listboxes = {}
        for server in self.servers:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=server)
            self.listboxes[server] = tk.Listbox(tab, width=50, height=20)
            self.listboxes[server].grid(row=0, column=0)

        self.update_data()
        self.after(5000, self.update_data)

    def update_data(self):
        for server in self.servers:
            self.listboxes[server].delete(0, tk.END)
            data = get_data(server)
            for station in data:
                if station['available']:
                    self.listboxes[server].insert(
                        tk.END, f'\u2705 {station["name"]}')
                else:
                    self.listboxes[server].insert(
                        tk.END, f'\u274C {station["name"]}')
        self.after(5000, self.update_data)


if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
