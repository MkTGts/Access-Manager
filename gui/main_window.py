import tkinter as tk
from tkinter import ttk, messagebox
from core.database import Database
from gui.entry_dialog import EntryDialog
from gui.section_dialog import SectionDialog
from gui.description_dialog import DescriptionDialog


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Access Manager v1.0.0")
        self.geometry("800x600")
        self.db = Database()
        
        self.create_widgets()
        self.load_sections()
        
        # Select first section if exists
        if self.sections_listbox.size() > 0:
            self.sections_listbox.selection_set(0)
            self.on_section_select(None)
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_field = ttk.Combobox(search_frame, values=["Название", "Логин"], state="readonly")
        self.search_field.current(0)
        self.search_field.pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="Искать", command=self.search_entries).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Очистить", command=self.clear_search).pack(side=tk.LEFT, padx=5)
        
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel
        left_frame = ttk.Frame(main_frame, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        
        ttk.Label(left_frame, text="Разделы:").pack(anchor=tk.W)
        self.sections_listbox = tk.Listbox(left_frame, height=20)
        self.sections_listbox.pack(fill=tk.BOTH, expand=True)
        self.sections_listbox.bind('<<ListboxSelect>>', self.on_section_select)
        self.sections_listbox.bind("<Double-1>", self.show_section_description)
        
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Добавить раздел", command=self.add_section).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Удалить раздел", command=self.delete_section).pack(fill=tk.X, pady=2)
        
        # Center panel
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(center_frame, text="Записи:").pack(anchor=tk.W)
        
        # Treeview for entries
        columns = ("name", "login", "password", "comment")
        self.entries_tree = ttk.Treeview(center_frame, columns=columns, show="headings", height=20)
        self.entries_tree.heading("name", text="Название")
        self.entries_tree.heading("login", text="Логин")
        self.entries_tree.heading("password", text="Пароль")
        self.entries_tree.heading("comment", text="Комментарий")
        
        self.entries_tree.column("name", width=150)
        self.entries_tree.column("login", width=150)
        self.entries_tree.column("password", width=150)
        self.entries_tree.column("comment", width=200)
        
        scrollbar = ttk.Scrollbar(center_frame, orient=tk.VERTICAL, command=self.entries_tree.yview)
        self.entries_tree.configure(yscroll=scrollbar.set)
        self.entries_tree.bind("<Double-1>", self.on_double_click)
        self.entries_tree.bind("<Button-3>", self.show_context_menu)
        
        self.entries_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons for entries
        entry_button_frame = ttk.Frame(center_frame)
        entry_button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(entry_button_frame, text="Добавить запись", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Редактировать запись", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Удалить запись", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
    
    def load_sections(self):
        self.sections_listbox.delete(0, tk.END)
        sections = self.db.get_sections()
        self.sections = {name: id for id, name, desc in sections}
        for name in self.sections:
            self.sections_listbox.insert(tk.END, name)
    
    def on_section_select(self, event):
        selection = self.sections_listbox.curselection()
        if selection:
            section_name = self.sections_listbox.get(selection[0])
            section_id = self.sections[section_name]
            self.load_entries(section_id)
    
    def show_section_description(self, event):
        selection = self.sections_listbox.curselection()
        if selection:
            section_name = self.sections_listbox.get(selection[0])
            section_id = self.sections[section_name]
            sections = self.db.get_sections()
            description = next((desc for id, name, desc in sections if id == section_id), "")
            DescriptionDialog(self, section_name, description)
    
    def load_entries(self, section_id):
        section_name = None
        for name, id in self.sections.items():
            if id == section_id:
                section_name = name
                break
        self.entries_tree.delete(*self.entries_tree.get_children())
        entries = self.db.get_entries(section_id)
        for entry in entries:
            values = list(entry[1:]) + [section_name]
            self.entries_tree.insert("", tk.END, iid=str(entry[0]), values=values)
    
    def add_section(self):
        dialog = SectionDialog(self, "Добавить раздел")
        if dialog.result:
            self.db.add_section(dialog.result['name'], dialog.result['description'])
            self.load_sections()
    
    def delete_section(self):
        selection = self.sections_listbox.curselection()
        if selection:
            section_name = self.sections_listbox.get(selection[0])
            if messagebox.askyesno("Удалить раздел", f"Удалить раздел '{section_name}' и все его записи?"):
                section_id = self.sections[section_name]
                self.db.delete_section(section_id)
                self.load_sections()
                self.entries_tree.delete(*self.entries_tree.get_children())
    
    def add_entry(self):
        selection = self.sections_listbox.curselection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите раздел")
            return
        section_name = self.sections_listbox.get(selection[0])
        section_id = self.sections[section_name]
        
        dialog = EntryDialog(self, "Добавить запись")
        if dialog.result:
            self.db.add_entry(section_id, **dialog.result)
            self.load_entries(section_id)
    
    def edit_entry(self):
        selected = self.entries_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись")
            return
        entry_id = int(selected[0])
        item = self.entries_tree.item(selected[0])
        values = item['values']
        entry_data = {
            'name': values[0],
            'login': values[1],
            'password': values[2],
            'comment': values[3]
        }
        
        dialog = EntryDialog(self, "Редактировать запись", entry_data)
        if dialog.result:
            self.db.update_entry(entry_id, **dialog.result)
            selection = self.sections_listbox.curselection()
            if selection:
                section_name = self.sections_listbox.get(selection[0])
                section_id = self.sections[section_name]
                self.load_entries(section_id)
    
    def delete_entry(self):
        selected = self.entries_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись")
            return
        if messagebox.askyesno("Удалить запись", "Удалить выбранную запись?"):
            entry_id = int(selected[0])
            self.db.delete_entry(entry_id)
            selection = self.sections_listbox.curselection()
            if selection:
                section_name = self.sections_listbox.get(selection[0])
                section_id = self.sections[section_name]
                self.load_entries(section_id)
    
    def search_entries(self):
        field = self.search_field.get()
        query = self.search_var.get().strip().lower()
        if not query:
            return
        field_map = {"Название": "name", "Логин": "login"}
        db_field = field_map.get(field)
        if not db_field:
            return
        results = self.db.search_entries(db_field, query)
        self.entries_tree.delete(*self.entries_tree.get_children())
        for result in results:
            section_name = None
            for sec_name, sec_id in self.sections.items():
                if sec_id == result[5]:
                    section_name = sec_name
                    break
            values = list(result[1:5]) + [section_name]
            self.entries_tree.insert("", tk.END, values=values)
        
    def clear_search(self):
        self.search_var.set("")
        selection = self.sections_listbox.curselection()
        if selection:
            section_name = self.sections_listbox.get(selection[0])
            section_id = self.sections[section_name]
            self.load_entries(section_id)
        else:
            self.entries_tree.delete(*self.entries_tree.get_children())

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Добавить запись", command=self.add_entry)
        selected = self.entries_tree.selection()
        if selected:
            menu.add_command(label="Редактировать запись", command=self.edit_entry)
            menu.add_command(label="Удалить запись", command=self.delete_entry)
        menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        self.edit_entry()
        
