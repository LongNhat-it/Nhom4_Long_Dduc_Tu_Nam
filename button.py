import tkinter as tk
from tkinter import ttk



class QLCafePage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.user_info = getattr(app_manager, 'current_user', {"username": "Guest", "role": "Nhân viên"})

        self.master.title("Hệ Thống Quản Lý Kho Cafe")
        self.master.geometry("1000x700")
        self.view()

    def view(self):
        # Header
        header = tk.Frame(self.master, bg="#6F4E37", height=60)
        header.pack(fill="x")

        tk.Label(header, text=f"Xin chào: {self.user_info['username']} ({self.user_info['role']})",
                 bg="#6F4E37", fg="white", font=("Arial", 10, "italic")).pack(side="right", padx=20)

        # Tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab Kho (Ai cũng xem được)
        self.tab_kho = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_kho, text="Quản lý Kho")
        self.build_kho_ui()

        # Tab Báo cáo (Chỉ Quản lý mới thấy)
        if self.user_info['role'] == "Quản lý":
            self.tab_bc = tk.Frame(self.notebook, bg="white")
            self.notebook.add(self.tab_bc, text="Báo Cáo & Cấu Hình")
            tk.Label(self.tab_bc, text="Dành cho Quản lý", font=("Arial", 14), bg="white").pack(pady=20)
            QLCafePage(self.tab_bc, text="Quản lý Tài khoản",
                         command=self.app_manager.show_quanlytk_page, style_type="info").pack()

    def build_kho_ui(self):
        # Bảng Treeview và các nút... (Code giống bản trước của bạn)
        tk.Label(self.tab_kho, text="Danh sách nguyên liệu", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
        # Nếu là nhân viên, vô hiệu hóa các nút Sửa/Xóa
        btn_state = "normal" if self.user_info['role'] == "Quản lý" else "disabled"
        QLCafePage(self.tab_kho, text="Thêm NL", state=btn_state).pack(side="left", padx=10)