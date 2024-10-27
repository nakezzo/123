import sqlite3

class DBINIT:
    def __init__(self, filename):
        """Инициализация этой залупы"""
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def users_exists(self, user_id):
        """Проверка на пидора"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT * FROM users WHERE id={user_id}""").fetchall()
            return bool(len(res))
        
    def add_user(self, user_id):
        """Добавляем гондона"""
        with self.connection:
            self.cursor.execute(f"""INSERT INTO users VALUES ({user_id}, 0, 0, 1) """)
            self.connection.commit()

    def get_active_users(self):
        """Получаем всех активных юзеров"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT id FROM users WHERE active=1""").fetchall()
            return res
    
    def get_users(self):
        """Получаем всех юзеров"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT id FROM users""").fetchall()
            return res
        
    def get_total(self, user_id):
        """Получить всего ставок"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT total FROM users WHERE id={user_id}""").fetchall()
            return res[0][0]
        
    def edit_total(self, user_id, amount):
        """Обновить тотал"""
        with self.connection:
            self.cursor.execute(f"""UPDATE users SET total={self.get_total(user_id) + amount} WHERE id={user_id}""")
            self.connection.commit()

    def get_moneyback(self, user_id):
        """Получить манибек"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT moneyback FROM users WHERE id={user_id}""").fetchall()
            return res[0][0]
        
    def edit_moneyback(self, user_id, amount):
        """Редачить манибэк"""
        with self.connection:
            self.cursor.execute(f"""UPDATE users SET moneyback={self.get_moneyback(user_id) + amount} WHERE id={user_id}""")
            self.connection.commit()

    def set_active(self, user_id, status = 1):
        """Установить актив"""
        with self.connection:
            self.cursor.execute(f"""UPDATE users SET active={status} WHERE id={user_id}""")
            self.connection.commit()

    def add_check(self, user_id, check_id):
        """Добавить чек"""
        with self.connection:
            self.cursor.execute(f"""INSERT INTO checks VALUES ({user_id}, {check_id}) """)
            self.connection.commit()

    def have_check(self, user_id):
        """Поиметь чек ой тоесть проверка на наличие"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT * FROM checks WHERE user_id={user_id}""").fetchall()
            return bool(len(res))
        
    def check_exists(self, check_id):
        """Сущетсвует ли чек с таким айди"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT * FROM checks WHERE check_id={check_id}""").fetchall()
            return bool(len(res))
        
    def remove_check(self, check_id):
        """Удалить чек"""
        with self.connection:
            self.cursor.execute(f"""DELETE FROM checks WHERE check_id={check_id} """)
            self.connection.commit()
    
    def get_check_id(self, user_id):
        """Получить айди чека"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT check_id FROM checks WHERE user_id={user_id}""").fetchone()
            return res[0]
        
    def get_checks(self):
        """Получить все чеки"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT check_id FROM checks""")
            ids=[]
            for r in res:
                ids.append(r[0])
            return ids
    
    def ban_user(self, user_id):
        """Забанить дебила"""
        with self.connection:
            self.cursor.execute(f"""INSERT INTO banned VALUES ({user_id})""")
            self.connection.commit()
    
    def deban_user(self, user_id):
        """Разбанить дебила"""
        with self.connection:
            self.cursor.execute(f"""DELETE FROM banned WHERE id={user_id} """)
            self.connection.commit()
    
    def get_bannned(self) -> list:
        """Получить список дебилов"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT id FROM banned""").fetchall()
            ids = []
            if len(res) > 0: 
                for r in res:
                    ids.append(r[0])
            return ids
    
    def add_mines(self, user_id, bad_mines, amount, asset, username):
        """Добавить мины. Крч, создать игру в бд."""
        with self.connection:
            self.cursor.execute(f"""INSERT INTO mines VALUES ({user_id}, "{str(bad_mines)}", {amount}, "{asset}", "{username}")""")
            self.connection.commit()
    
    def get_data_mines(self, user_id) -> dict:
        """Получить сумму валюту и юз чела из мин"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT amount, asset, username FROM mines WHERE id={user_id}""").fetchall()
            return {"amount": res[0][0], "asset": res[0][1], "username": res[0][2]}
        
    def get_bad_mines(self, user_id):
        """Получить корды мин"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT bad FROM mines WHERE id={user_id}""").fetchall()
            return eval(res[0][0])
    
    def user_played_mines(self, user_id):
        """Проверка на то, играет ли игрок в мину"""
        with self.connection:
            res = self.cursor.execute(f"""SELECT * FROM mines WHERE id={user_id}""").fetchall()
            return bool(len(res))
    
    def remove_mines(self, user_id):
        """Удалить игру из бд"""
        with self.connection:
            self.cursor.execute(f"""DELETE FROM mines WHERE id={user_id} """)
            self.connection.commit()