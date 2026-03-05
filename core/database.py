import sqlite3
import os


class Database:
    def __init__(self, db_path='access_manager.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id INTEGER,
                    name TEXT,
                    login TEXT,
                    password TEXT,
                    comment TEXT,
                    FOREIGN KEY (section_id) REFERENCES sections (id)
                )
            ''')
            conn.commit()

    def get_sections(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, description FROM sections')
            return cursor.fetchall()

    def add_section(self, name, description):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sections (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            return cursor.lastrowid

    def delete_section(self, section_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM entries WHERE section_id = ?', (section_id,))
            cursor.execute('DELETE FROM sections WHERE id = ?', (section_id,))
            conn.commit()

    def get_entries(self, section_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, login, password, comment FROM entries WHERE section_id = ?', (section_id,))
            return cursor.fetchall()

    def add_entry(self, section_id, name, login, password, comment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO entries (section_id, name, login, password, comment) VALUES (?, ?, ?, ?, ?)',
                           (section_id, name, login, password, comment))
            conn.commit()
            return cursor.lastrowid

    def update_entry(self, entry_id, name, login, password, comment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE entries SET name = ?, login = ?, password = ?, comment = ? WHERE id = ?',
                           (name, login, password, comment, entry_id))
            conn.commit()

    def delete_entry(self, entry_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
            conn.commit()

    def search_entries(self, field, query):
        field_map = {'name': 'name', 'login': 'login'}
        if field not in field_map:
            return []
        column = field_map[field]
        query_lower = query.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT id, name, login, password, comment, section_id FROM entries WHERE LOWER({column}) LIKE ?',
                           ('%' + query_lower + '%',))
            return cursor.fetchall()