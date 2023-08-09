import requests
import tkinter as tk
from tkinter import messagebox

class TmproxyForm:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_api_request(self, url, params):
        try:
            response = requests.post(url, json=params)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            messagebox.showinfo("Error", f"Error: {e}")
            return None

    def get_current_proxy(self):
        data = self.send_api_request("https://tmproxy.com/api/proxy/get-current-proxy", {"api_key": self.api_key})
        if data:
            messagebox.showinfo("Current Proxy", f"Proxy HTTPS: {data['https']}")
        else:
            messagebox.showinfo("Error", "Unable to get proxy.")

class TmproxyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TMProxy - By EpChannel")
        self.geometry("300x200")
        self.api_key = "API-KEY-CUA-BAN"  # Replace with your API Key
        self.form = TmproxyForm(self.api_key)
        self.btn_get_current_proxy = tk.Button(self, text="Xem địa chỉ IP hiện tại", command=self.form.get_current_proxy)
        self.btn_get_current_proxy.pack(pady=10)
        self.lbl_copyright = tk.Label(self, text="Copyright © 2023 EpChannel")
        self.lbl_copyright.pack(pady=5)

if __name__ == "__main__":
    TmproxyGUI().mainloop()