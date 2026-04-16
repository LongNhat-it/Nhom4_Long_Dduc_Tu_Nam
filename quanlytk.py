import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

from common.button import QLCafePage


class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("Quản lý tài khoản")
        self.master.geometry("600x400")

    def view(self):
        # Title
        title_label = tk.Label(self.master, text="Quản lý tài khoản", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        # Buttons
        refresh_btn = QLCafePage(button_frame, text="Làm mới", command=self.load_accounts, style_type="info")
        refresh_btn.pack(side="left", padx=5)

        delete_btn = QLCafePage(button_frame, text="Xóa tài khoản", command=self.delete_account, style_type="danger")
        delete_btn.pack(side="left", padx=5)

        edit_btn = QLCafePage(button_frame, text="Sửa tài khoản", command=self.edit_account, style_type="warning")
        edit_btn.pack(side="left", padx=5)

        back_btn = QLCafePage(button_frame, text="Quay lại", command=self.back_to_login, style_type="secondary")
        back_btn.pack(side="right", padx=5)

        # Frame for treeview
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Treeview for displaying accounts
        columns = ("STT", "Username", "Password")
        self.account_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.account_tree.heading("STT", text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")

        # Configure column widths
        self.account_tree.column("STT", width=50, anchor="center")
        self.account_tree.column("Username", width=200, anchor="center")
        self.account_tree.column("Password", width=200, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.account_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # Status bar
        self.status_label = tk.Label(self.master, text="Sẵn sàng", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def load_accounts(self):
        """Load accounts from CSV file and display in treeview"""
        # Clear existing items
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)

        try:
            database_path = "database/tk.csv"
            if not os.path.exists(database_path):
                self.status_label.config(text="Chưa có dữ liệu tài khoản")
                return

            with open(database_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                accounts = list(csv_reader)
                
                if not accounts:
                    self.status_label.config(text="Không có tài khoản nào")
                    return

                for idx, account in enumerate(accounts, 1):
                    if len(account) >= 2:  # Ensure account has username and password
                        self.account_tree.insert("", "end", values=(idx, account[0], account[1]))

                self.status_label.config(text=f"Đã tải {len(accounts)} tài khoản")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            self.status_label.config(text="Lỗi tải dữ liệu")

    def delete_account(self):
        """Delete selected account"""
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần xóa")
            return

        # Get selected account info
        item_values = self.account_tree.item(selected_item[0], "values")
        username = item_values[1]

        # Confirm deletion
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản '{username}'?"):
            try:
                self.remove_account_from_file(username)
                self.load_accounts()  # Refresh the list
                messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa tài khoản: {str(e)}")

    def remove_account_from_file(self, username_to_remove):
        """Remove account from CSV file"""
        database_path = "database/tk.csv"
        temp_path = "database/tk_temp.csv"
        
        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            for row in csv_reader:
                if len(row) >= 2 and row[0] != username_to_remove:
                    csv_writer.writerow(row)
        
        # Replace original file with temp file
        os.replace(temp_path, database_path)

    def edit_account(self):
        """Edit selected account"""
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần sửa")
            return

        # Get selected account info
        item_values = self.account_tree.item(selected_item[0], "values")
        old_username = item_values[1]
        old_password = item_values[2]

        # Navigate to edit page
        self.app_manager.show_suatk_page(old_username, old_password)

    def back_to_login(self):
        """Return to login page"""
        self.app_manager.show_login_page()
