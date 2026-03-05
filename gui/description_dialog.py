import tkinter as tk
from tkinter import ttk


class DescriptionDialog(tk.Toplevel):
    def __init__(self, parent, section_name, description):
        super().__init__(parent)
        self.title(f"Описание раздела: {section_name}")
        self.geometry("300x150")
        self.resizable(False, False)
        
        ttk.Label(self, text="Описание:", font=("Arial", 10, "bold")).pack(pady=10)
        text = tk.Text(self, height=4, wrap=tk.WORD)
        text.insert(tk.END, description)
        text.config(state=tk.DISABLED)
        text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        ttk.Button(self, text="Закрыть", command=self.destroy).pack(pady=10)
        
        self.center_window()
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")