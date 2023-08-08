# --------------------------------------------------------------------------------
# TOOL CHECK TMPROXY
# Tool có 2 chức năng: Xem địa chỉ IP hiện tại và Lấy địa chỉ IP mới
# Copyright (C) 2023 EPCHANNEL 07/08/2023
# Nếu thấy tool hay cho mình 1 Star trên Github nha :3 
# Cài đầy đủ các thư viện
import requests
import tkinter as tk
from tkinter import messagebox
import pyperclip

# --------------------------------------------------------------------------------
class TmproxyForm:
    def __init__(self, api_key_var):
        self.api_key_var = api_key_var
        self.proxy = None

        # Create buttons for copying proxy information
        self.socks5_button = tk.Button(text="Copy SOCKS5 Proxy", command=self.copy_socks5, state="disabled")
        self.https_button = tk.Button(text="Copy HTTPS Proxy", command=self.copy_https, state="disabled")

        # You need to place these buttons on your tkinter window
        self.socks5_button.pack()
        self.https_button.pack()

    def get_current_proxy(self):
        api_key = self.api_key_var.get()
        url = "https://tmproxy.com/api/proxy/get-current-proxy"
        request_body = {"api_key": api_key}
        response = requests.post(url, json=request_body)
        if response.status_code == 200:
            response_json = response.json()
            self.proxy = response_json["data"]
            messagebox.showinfo("Current Proxy", 
                                f"Địa chỉ IP thật: {self.proxy['ip_allow']}\n"
                                f"Tên khu vực: {self.proxy['location_name']}\n"
                                f"Proxy SOCKS5: {self.proxy['socks5']}\n"
                                f"Proxy HTTPS: {self.proxy['https']}\n"
                                f"Thời gian còn sống của proxy: {self.proxy['timeout']} giây\n"
                                f"Thời gian đổi IP tiếp theo: {self.proxy['next_request']} giây\n"
                                f"Hết hạn vào: {self.proxy['expired_at']}")

            # Enable the copy buttons if the API call was successful
            self.socks5_button['state'] = 'normal'
            self.https_button['state'] = 'normal'

            with open('api_key.txt', 'w') as f:
                f.write(api_key)
        else:
            messagebox.showinfo("Error", f"Lỗi trong quá trình gửi yêu cầu API: {response.status_code}")

    def copy_socks5(self):
        if self.proxy:
            pyperclip.copy(self.proxy['socks5'])
            messagebox.showinfo("Copied", "Proxy SOCKS5 đã được copy vào clipboard.")

    def copy_https(self):
        if self.proxy:
            pyperclip.copy(self.proxy['https'])
            messagebox.showinfo("Copied", "Proxy HTTPS đã được copy vào clipboard.")


    def get_new_proxy(self):
        api_key = self.api_key_var.get()
        param = {"api_key": api_key, "sign": "string"}
        response = requests.post("https://tmproxy.com/api/proxy/get-new-proxy", json=param)
        data = response.json()
        if data["data"]["https"]:
            self.proxy = data["data"]
            messagebox.showinfo("New Proxy", f"New Proxy: {self.proxy['https']}")
            with open('api_key.txt', 'w') as f:
                f.write(api_key)
        else:
            messagebox.showinfo("Wait", f"Vui lòng chờ thời gian đổi ip: {self.proxy['next_request']} giây")


class TmproxyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TMProxy - By EpChannel")
        self.geometry("300x200")
        self.api_key_var = tk.StringVar()
        try:
            with open('api_key.txt', 'r') as f:
                stored_api_key = f.read().strip()
                self.api_key_var.set(stored_api_key)
        except FileNotFoundError:
            pass
        self.form = TmproxyForm(self.api_key_var)
        self.lbl_api_key = tk.Label(self, text="Nhập API Key:")
        self.lbl_api_key.pack(pady=5)
        self.entry_api_key = tk.Entry(self, textvariable=self.api_key_var)
        self.entry_api_key.pack(pady=5)
        self.btn_get_current_proxy = tk.Button(self, text="Xem địa chỉ IP hiện tại", command=self.form.get_current_proxy)
        self.btn_get_new_proxy = tk.Button(self, text="Lấy IP mới", command=self.form.get_new_proxy)
        self.btn_get_current_proxy.pack(pady=10)
        self.btn_get_new_proxy.pack(pady=10)
        self.lbl_copyright = tk.Label(self, text="Copyright © 2023 EpChannel")
        self.lbl_copyright.pack(pady=5)

if __name__ == "__main__":
    TmproxyGUI().mainloop()