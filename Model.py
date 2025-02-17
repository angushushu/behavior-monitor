import os
import sqlite3
import numpy as np
from datetime import date

class Model:
    def __init__(self):
        self.db_path = os.path.dirname(__file__) + '\list.db' # move to controller?
        self.date = date.today()
        self.steps = dict() #[(task:step)]
    
    def get_date(self):
        return self.date

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists tasks(
            taskid INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT
            )""")
        c.execute("""CREATE TABLE if not exists records(
            date TEXT,
            taskid INTEGER,
            time INTEGER,
            FOREIGN KEY(taskid) REFERENCES tasks(taskid) ON DELETE CASCADE
            )""")
        conn.commit()
        conn.close()
    
    def get_tasks(self):
        return self.steps.keys()

    def load_records(self, *, tasks=None, date=None):
        check = None
        if tasks is not None:
            check = f"WHERE task='{tasks[0]}'" if len(tasks) == 1 else f"WHERE task IN {str(tuple(tasks))}"
            # check = f"""WHERE task IN {list}"""
        elif date is not None:
            check = f"""WHERE records.date="{str(date)}" """
        else:
            raise TypeError("Only one of (tasks, date) should be filled")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT tasks.task, records.date, records.time
            FROM tasks, records
            {check} AND tasks.taskid=records.taskid
        """)
        records = cur.fetchall()
        conn.commit()
        conn.close()
        return records

    def load_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(f"""SELECT task FROM tasks""")
        tasks = cur.fetchall()
        # print('tasks',tasks)
        for t in tasks:
            self.steps[t[0]] = 0
        conn.commit()
        conn.close()
        # print(self.steps)
        return tasks
    
    def load_dates(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT records.date
            FROM records
        """)
        dates = cur.fetchall()
        conn.commit()
        conn.close()
        return dates

    def get_table_data(self, tasks):
        records = self.load_records(tasks=tasks)
        date_total = dict()
        for i in records:
            if i[1] in date_total:
                date_total[i[1]] += i[2]
            else:
                date_total[i[1]] = i[2]
        table_data = np.zeros((len(date_total), len(tasks)), dtype='float64')
        for r in records:
            table_data[list(date_total).index(r[1])][tasks.index(r[0])] = r[2]
        temp = np.array([list(date_total.values())])
        table_data = np.concatenate((table_data, temp.T), axis=1)
        col_max = table_data.max(axis=0)
        perc_data = np.divide(table_data, col_max, out=np.zeros_like(table_data), where=col_max!=0)
        perc_data *= 100
        return table_data, perc_data, date_total
    
    def load_steps(self):
        self.steps.clear()
        self.load_tasks()
        records = self.load_records(date=date.today())
        print('records', records)
        for record in records:
            self.steps[record[0]] = record[2]
        return self.steps

    def exist_task(self, task):
        return task in self.steps
    
    def get_tasks(self):
        return self.steps.keys()

    def add_task(self, task):
        if self.exist_task(task):
            return
        else:
            self.steps[task] = 0
    
    def rename_task(self, old, new):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # change name, but not the records
        print(old, new)
        cur.execute(f"""
            UPDATE tasks
            SET task="{new}"
            WHERE task="{old}"
        """)
        self.steps[new] = self.steps.pop(old)
        conn.commit()
        conn.close()

    def remove_task(self, task):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()
        c.execute(f"""
            DELETE FROM tasks
            WHERE tasks.task="{task}"
        """)
        conn.commit()
        conn.close()
        self.steps.pop(task)

    def save_records(self):
        self.date = date.today()
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()
        c.execute(f"""
            DELETE FROM records
            WHERE date="{str(self.date)}";
        """,)
        for task in self.steps:
            c.execute(f"""
                SELECT EXISTS(SELECT 1 from tasks where task="{task}")
            """)
            if c.fetchone()[0] == 0:
                c.execute(f"""
                    INSERT INTO tasks (task)
                    VALUES ("{task}")
                """)
            c.execute(f"""
                SELECT taskid from tasks where task="{task}"
            """)
            res = c.fetchone()
            task_id = res[0]
            c.execute("""INSERT INTO records VALUES 
                (:date,:task,:time)
            """,
                {
                    'date': str(self.date),
                    'task': task_id,
                    'time': self.steps[task]
                })
        conn.commit()
        conn.close()
    
    def clear_all(self):
        self.steps.clear()
        # self.date = date.today()
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()
        c.execute(f"""
            DELETE FROM tasks
        """)
        conn.commit()
        conn.close()
    
    def update_step(self, task, step):
        self.steps[task] = step
    
    def get_max_step(self):
        return max(self.steps.values()) if len(self.steps) > 0 else None

    def date_change(self):
        self.date = date.today()
        for t in self.steps:
            self.steps[t] = 0