import tkinter as tk
from tkinter import ttk


class SectionDialog(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        
        self.result = None
        
        ttk.Label(self, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self, text="Описание:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.desc_var).grid(row=1, column=1, padx=10, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
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
    
    def save(self):
        name = self.name_var.get().strip()
        if name:
            self.result = {
                'name': name,
                'description': self.desc_var.get().strip()
            }
            self.destroy()
        else:
            tk.messagebox.showerror("Ошибка", "Название раздела не может быть пустым")
    
    def cancel(self):
        self.result = None
        self.destroy()