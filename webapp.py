
import streamlit as aw
import sqlite3 as sq
import datetime
import json
import pandas as pd
from collections import Counter
def init_db():
    conn = sq.connect("data.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS MARK
                 (name TEXT, subject TEXT, attendstatus TEXT, attend_count INTEGER,
                 PRIMARY KEY (name, subject))''')

    conn.commit()
    return conn, c

conn, cursor = init_db()

aw.title("Attendance Tracker")

option = aw.sidebar.selectbox("Select an option",
    ["Mark Attendance", "View attendance for all subjects", "View attendance for specific subject"],
    placeholder="Select option...")

if option == "Mark Attendance":
    aw.header("Mark Attendance")
    col1, col2 = aw.columns(2)

    with col1:
        name = aw.text_input("Enter student name", placeholder="Enter name")

    with col2:
        subject = aw.text_input("Enter subject", placeholder="Enter subject")
    col3, col4 = aw.columns(2)

    with col3:
        if aw.button("Present", type="primary", use_container_width=True):
            if name and subject:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                try:

                    cursor.execute("SELECT attendstatus FROM MARK WHERE name=? AND subject=?", (name, subject))
                    result = cursor.fetchone()

                    if result:
                        attendstatus = json.loads(result[0])
                        attendstatus[date] = "present"
                        cursor.execute("""
                            UPDATE MARK 
                            SET attend_count = attend_count + 1, attendstatus = ? 
                            WHERE name = ? AND subject = ?
                        """, (json.dumps(attendstatus), name, subject))
                    else:
                        attendstatus = {date: "present"}
                        cursor.execute("""
                            INSERT INTO MARK(name, subject, attendstatus, attend_count) 
                            VALUES(?, ?, ?, ?)
                        """, (name, subject, json.dumps(attendstatus), 1))

                    conn.commit()
                    aw.success(f"✅ Marked {name} present for {subject}")
                except Exception as e:
                    aw.error(f"❌ Error: {e}")
            else:
                aw.warning("Please fill in both name and subject.")

    with col4:
        if aw.button("Absent", type="secondary", use_container_width=True):
            if name and subject:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                try:
                    cursor.execute("SELECT attendstatus FROM MARK WHERE name=? AND subject=?", (name, subject))
                    result = cursor.fetchone()

                    if result:
                        attendstatus = json.loads(result[0])
                        attendstatus[date] = "absent"
                        cursor.execute("""
                            UPDATE MARK 
                            SET attendstatus = ? 
                            WHERE name = ? AND subject = ?
                        """, (json.dumps(attendstatus), name, subject))
                    else:
                        attendstatus = {date: "absent"}
                        cursor.execute("""
                            INSERT INTO MARK(name, subject, attendstatus, attend_count) 
                            VALUES(?, ?, ?, ?)
                        """, (name, subject, json.dumps(attendstatus), 0))

                    conn.commit()
                    aw.success(f"✅ Marked {name} absent for {subject}")
                except Exception as e:
                    aw.error(f"❌ Error: {e}")
            else:
                aw.warning("Please fill in both name and subject.")
elif option == "View attendance for all subjects":
                aw.header("view attendance")

                search_name = aw.text_input("enter a student name", placeholder="enter student name")
                if search_name:
                    try:

                        att = cursor.execute("SELECT name ,subject, attendstatus, attend_count FROM MARK WHERE name=?",
                                             (search_name,))
                        records = att.fetchall()
                        if records:
                            for record in records:
                                name, subject, attendstatus, attend_count = record
                                attendance_dict = json.loads(attendstatus)
                                status_list = list(attendance_dict.values())
                                count = Counter(status_list)

                                present_count = count.get("present", 0)
                                absent_count = count.get("absent", 0)

                                aw.markdown(f"""
                                        <div style="border:1px solid #ccc; padding:10px; border-radius:8px; background:black;">
                                        <b>🧑 Name:</b> {name}<br>
                                        <b>📚 Subject:</b> {subject}<br>
                                        <b>📅 Total Presents:</b> {present_count}
                                         <b>📅 Total absent:</b> {absent_count}
                                        </div>
                                    """, unsafe_allow_html=True)

                                attendance_dict = json.loads(attendstatus)
                                attendance_data = []

                                for date, status in attendance_dict.items():
                                    attendance_data.append({
                                        "name":name,
                                        "subject":subject,
                                        "Date": date,
                                        "Status": status.title()
                                    })

                                if attendance_data:
                                    df = pd.DataFrame(attendance_data)
                                    df = df.sort_values(by="Date", ascending=False)


                                    def color_status(val):
                                        color = "black" if val == "Present" else "#ffc7ce"
                                        return f"background-color: {color}"


                                    aw.dataframe(
                                        df.style.applymap(color_status, subset=["Status"]),
                                        use_container_width=True
                                    )

                                    total = len(attendance_dict)
                                    present = sum(1 for s in attendance_dict.values() if s.lower() == "present")
                                    percentage = (present / total) * 100 if total > 0 else 0

                                    aw.metric(
                                        label="Attendance Percentage",
                                        value=f"{percentage:.1f}%",
                                        delta=f"{present}/{total} days present"
                                    )
                                else:
                                    aw.info("No attendance records found for this subject",subject)
                        else:
                            aw.info("No records found for this student")
                    except Exception as e:
                        aw.error(f"Error: {str(e)}")
else:
                        name = aw.text_input("Enter student name", placeholder="Name")
                        sub = aw.text_input("Enter subject", placeholder="Enter the subject")

                        if name and sub:
                            try:
                                att = cursor.execute(
                                    "SELECT name, subject, attendstatus, attend_count FROM MARK WHERE name=? AND subject=?",
                                    (name, sub)
                                )
                                record = att.fetchone()

                                if record:
                                    name, subject, attendstatus, attend_count = record
                                    attendance_dict = json.loads(attendstatus)
                                    status_list = list(attendance_dict.values())
                                    count = Counter(status_list)

                                    present_count = count.get("present", 0)
                                    absent_count = count.get("absent", 0)

                                    aw.markdown(f"""
                                            <div style="border:1px solid #ccc; padding:10px; border-radius:8px; background:black;">
                                            <b>🧑 Name:</b> {name}<br>
                                            <b>📚 Subject:</b> {subject}<br>
                                            <b>✅ Presents:</b> {present_count}<br>
                                            <b>❌ Absents:</b> {absent_count}
                                            </div>
                                        """, unsafe_allow_html=True)

                                    attendance_data = []
                                    for date, status in attendance_dict.items():
                                        attendance_data.append({
                                            "name": name,
                                            "subject": subject,
                                            "Date": date,
                                            "Status": status.title()
                                        })

                                    if attendance_data:
                                        df = pd.DataFrame(attendance_data)
                                        df = df.sort_values(by="Date", ascending=False)


                                        def color_status(val):
                                            return "background-color: #c6efce" if val == "Present" else "background-color: #ffc7ce"


                                        aw.dataframe(
                                            df.style.applymap(color_status, subset=["Status"]),
                                            use_container_width=True
                                        )

                                        total = len(attendance_dict)
                                        present = sum(1 for s in attendance_dict.values() if s.lower() == "present")
                                        percentage = (present / total) * 100 if total > 0 else 0

                                        aw.metric(
                                            label="Attendance Percentage",
                                            value=f"{percentage:.1f}%",
                                            delta=f"{present}/{total} days present"
                                        )
                                    else:
                                        aw.info("No attendance records found.")
                                else:
                                    aw.warning("No records found for this student and subject.")
                            except Exception as e:
                                aw.error(f"Error: {str(e)}")





