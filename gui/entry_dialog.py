import tkinter as tk
from tkinter import ttk
from core.password_generator import generate_password


class EntryDialog(tk.Toplevel):
    def __init__(self, parent, title, entry_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.result = None
        
        # Fields
        ttk.Label(self, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_var = tk.StringVar(value=entry_data.get('name', '') if entry_data else '')
        ttk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self, text="Логин:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.login_var = tk.StringVar(value=entry_data.get('login', '') if entry_data else '')
        ttk.Entry(self, textvariable=self.login_var).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self, text="Пароль:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.password_var = tk.StringVar(value=entry_data.get('password', '') if entry_data else '')
        password_entry = ttk.Entry(self, textvariable=self.password_var)
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Button(self, text="Сгенерировать пароль", command=self.generate_password).grid(row=2, column=2, padx=10, pady=5)
        
        ttk.Label(self, text="Комментарий:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.comment_var = tk.StringVar(value=entry_data.get('comment', '') if entry_data else '')
        ttk.Entry(self, textvariable=self.comment_var).grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=self.cancel).pack(side=tk.LEFT, padx=10)
        
        self.transient(parent)
        self.grab_set()
        self.center_window()
        self.wait_window(self)
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
    
    def generate_password(self):
        password = generate_password()
        self.password_var.set(password)
    
    def save(self):
        self.result = {
            'name': self.name_var.get(),
            'login': self.login_var.get(),
            'password': self.password_var.get(),
            'comment': self.comment_var.get()
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()