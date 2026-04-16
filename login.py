import tkinter as tk
from tkinter import messagebox
import csv
from common.button import QLCafePage


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.master.title("Đăng nhập - Cafe System")
        self.master.geometry("400x500")
        self.master.configure(bg="white")
        self.view()

    def view(self):
        tk.Label(self.master, text="☕", font=("Arial", 50), bg="white", fg="#6F4E37").pack(pady=(30, 0))
        tk.Label(self.master, text="ĐĂNG NHẬP", font=("Arial", 18, "bold"), bg="white", fg="#3D2B1F").pack(pady=20)

        container = tk.Frame(self.master, bg="white")
        container.pack(fill="x", padx=50)

        tk.Label(container, text="Username:", bg="white", fg="#6F4E37", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_username = tk.Entry(container, font=("Arial", 11), bg="#F8F9FA", bd=1)
        self.entry_username.pack(fill="x", ipady=8, pady=(5, 15))

        tk.Label(container, text="Password:", bg="white", fg="#6F4E37", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_password = tk.Entry(container, font=("Arial", 11), bg="#F8F9FA", bd=1, show="*")
        self.entry_password.pack(fill="x", ipady=8, pady=(5, 20))

        QLCafePage(self.master, text="ĐĂNG NHẬP", command=self.login, style_type="primary").pack(fill="x", padx=50,
                                                                                                   ipady=5)
        QLCafePage(self.master, text="Tạo tài khoản mới", command=self.tao_tk, style_type="success").pack(fill="x",
                                                                                                            padx=50,
                                                                                                            pady=10,
                                                                                                            ipady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            with open("database/tk.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        u, p, r = row[0], row[1], row[2]
                        if username == u and password == p:
                            # Lưu thông tin user hiện tại vào app_manager
                            self.app_manager.current_user = {"username": u, "role": r}
                            self.app_manager.show_main_page()  # Chuyển sang QLCafe.py
                            return
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Chưa có dữ liệu tài khoản. Hãy đăng ký!")

    def tao_tk(self):
        self.app_manager.show_taotk_page()