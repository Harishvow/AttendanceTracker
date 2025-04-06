import json
import sqlite3 as sq
import datetime
from datetime import date
from sqlite3 import connect
from tkinter.constants import INSERT

from streamlit import connection
import orjson

class AttendanceTracker:
    def __init__(self):
        self.conn = sq.connect("data.db")
        self.cursor = self.conn.cursor()

    def get_attendance(self, name, sub):
        self.cursor.execute("SELECT attendstatus FROM MARK WHERE name=? AND subject=?", (name, sub,))
        att = self.cursor.fetchone()
        print(att)
        return att[0] if att else "{}"

    def mark_attendance(self, name, sub1, ap):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        raw_attendstatus = str(self.get_attendance(name, sub1))
        attendstatus =json.loads(raw_attendstatus)
        print(attendstatus)
        attendstatus[date] = f"{ap}"
        self.cursor.execute("SELECT attend_count FROM MARK WHERE subject = ? AND name = ?", (sub1, name))
        row = self.cursor.fetchone()
        print(attendstatus)
        if row:
            self.cursor.execute("UPDATE MARK SET attend_count = attend_count + 1,attendstatus=? WHERE name = ? AND subject = ?",
                                (str(attendstatus), name, sub1))
        else:
            self.cursor.execute("INSERT INTO MARK(name, attendstatus, subject, attend_count) VALUES(?, ?, ?, ?)",
                                (name, str(attendstatus), sub1, 1))
        self.conn.commit()

    """else:
            save=self.attendance_list[name].append(name)
            print(f"{name} is marked present today{date}")"""

    def view_attendance(self, name):
        att =  self.cursor.execute("SELECT name ,attendstatus FROM MARK WHERE name=?", (name,))
        x = att.fetchone()
        print(x)

        """if not self.attendance_list:
            print("no records found")
        else:
            print("attendance list:")
            for name , date in self.attendance_list.items():
                print(F"{name}:{",".join(date)}")"""

    def view_specific(self, name):

        att = self.cursor.execute(f"select * from MARK where name=?", (name,))
        x = att.fetchall()
        print(x)
        """if name in self.attendance_list:
            date in self.attendance_list
            print(f"{name} is present on{",".join(date)}")"""

    def run(self):
        while True:
            print("1.mark_attendance")
            print("2.view_attendance")
            print("3.view_attendance")

            choice = input("enter the choice ")
            if choice == "1":
                name = input("enter the student name:")
                sub1 = input("enter the Subject name")
                ap = input("enter the student present/absent:")
                self.mark_attendance(name, sub1, ap)

            elif choice == "2":
                name = input("enter the student name:")
                self.view_attendance(name)
            elif choice == "3":
                name = input("enter the student name:")
                self.view_specific(name)
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    system = AttendanceTracker()
    system.run()





























