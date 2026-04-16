import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from common.button import QLCafePage


class TaoTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.master.title("Đăng ký tài khoản")
        self.master.geometry("400x550")
        self.master.configure(bg="white")
        self.view()

    def view(self):
        tk.Label(self.master, text="TẠO TÀI KHOẢN", font=("Arial", 18, "bold"), bg="white", fg="#6F4E37").pack(pady=30)

        container = tk.Frame(self.master, bg="white")
        container.pack(fill="x", padx=50)

        tk.Label(container, text="Username:", bg="white").pack(anchor="w")
        self.entry_username = tk.Entry(container, font=("Arial", 11))
        self.entry_username.pack(fill="x", ipady=5, pady=5)

        tk.Label(container, text="Password:", bg="white").pack(anchor="w")
        self.entry_password = tk.Entry(container, show="*", font=("Arial", 11))
        self.entry_password.pack(fill="x", ipady=5, pady=5)

        tk.Label(container, text="Chức vụ:", bg="white").pack(anchor="w")
        self.cb_role = ttk.Combobox(container, values=["Nhân viên", "Quản lý"], state="readonly")
        self.cb_role.pack(fill="x", ipady=5, pady=5)
        self.cb_role.set("Nhân viên")

        QLCafePage(self.master, text="Xác nhận Đăng ký", command=self.tao_tk, style_type="primary").pack(fill="x",
                                                                                                           padx=50,
                                                                                                           pady=(20,
                                                                                                                 10))
        QLCafePage(self.master, text="Quay lại Đăng nhập", command=self.back_login, style_type="secondary").pack(
            fill="x", padx=50)

    def tao_tk(self):
        u = self.entry_username.get()
        g = self.entry_gmail.get()
        p = self.entry_password.get()

        if not u or not g or not p:
            messagebox.warning("!", "Vui lòng nhập đủ thông tin")
            return

        file_path = "database/tk.csv"
        file_exists = os.path.isfile(file_path)

        try:
            with open(file_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                if not file_exists or os.stat(file_path).st_size == 0:
                     writer.writerow(["hoten" + "," + "gmail" + "," + "matkhau"])

                writer.writerow([u + "," + g + "," + p])

            messagebox.showinfo("Thành công", f"Đã tạo tài khoản {u}!")
            self.app_manager.show_login_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")

    def back_login(self):
        self.app_manager.show_login_page()