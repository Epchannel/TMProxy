# --------------------------------------------------------------------------------
# TOOL CHECK TMPROXY
# Tool có 2 chức năng: Xem địa chỉ IP hiện tại và Lấy địa chỉ IP mới
# Copyright (C) 2023 EPCHANNEL 07/08/2023
# Nếu thấy tool hay cho mình 1 Star trên Github nha :3 
# Cài đầy đủ các thư viện
import requests
import tkinter as tk
from tkinter import messagebox
# --------------------------------------------------------------------------------
class TmproxyForm:
    def __init__(self, api_key_var):
        self.api_key_var = api_key_var
        self.proxy = None

    def get_current_proxy(self):
        api_key = self.api_key_var.get()
        url = "https://tmproxy.com/api/proxy/get-current-proxy"
        request_body = {"api_key": api_key}
        response = requests.post(url, json=request_body)
        if response.status_code == 200:
            response_json = response.json()
            self.proxy = response_json["data"]
            messagebox.showinfo("Current Proxy", f"Địa chỉ IP thật: {self.proxy['ip_allow']}\n"
                                                  f"Proxy Fake: {self.proxy['https']}\n"
                                                  f"Thời gian đổi ip tiếp theo: {self.proxy['next_request']} giây\n"
                                                  f"Hết hạn vào: {self.proxy['expired_at']}")
            with open('api_key.txt', 'w') as f:
                f.write(api_key)
        else:
            messagebox.showinfo("Error", f"Lỗi trong quá trình gửi yêu cầu API: {response.status_code}")

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