import tkinter as tk
from tkinter import ttk
import sqlite3


# =====================================
# ส่วนที่ 1: เชื่อมต่อฐานข้อมูล SQLite
# =====================================

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


# สร้างตาราง user ถ้ายังไม่มี
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

conn.commit()


# =====================================
# ส่วนที่ 2: ฟังก์ชันบันทึกข้อมูล
# =====================================

def save_data():

    # ดึงข้อมูลจากช่องกรอก
    name = entry_name.get()
    age = entry_age.get()

    # ตรวจสอบว่ากรอกข้อมูลครบหรือไม่
    if name and age:

        # เพิ่มข้อมูลลงฐานข้อมูล
        cursor.execute(
            "INSERT INTO user (name, age) VALUES (?, ?)",
            (name, age)
        )

        # บันทึกข้อมูลจริงลง Database
        conn.commit()

        # แสดงข้อมูลใน Treeview
        tree.insert("", "end", values=(name, age))

        # ล้างข้อมูลในช่องกรอก
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)


# =====================================
# ส่วนที่ 3: ฟังก์ชันโหลดข้อมูล
# =====================================

def load_data():

    # ล้างข้อมูลเก่า
    for item in tree.get_children():
        tree.delete(item)

    # ดึง ID + ชื่อ + อายุ
    cursor.execute(
        "SELECT id, name, age FROM user"
    )

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

# =====================================
# ส่วนที่ : ฟังก์ชันโหลดลบข้อมูล
# =====================================

def delete_data():

    # ดูว่าเลือกแถวไหน
    selected_item = tree.selection()

    # ถ้ายังไม่ได้เลือก
    if not selected_item:
        print("กรุณาเลือกข้อมูลก่อน")
        return

    # ดึงข้อมูลจากแถวที่เลือก
    item = tree.item(selected_item[0])

    # ดึงค่าจากแถว
    values = item["values"]

    # ค่าแรกคือ ID
    user_id = values[0]

    # ลบข้อมูลจาก Database
    cursor.execute(
        "DELETE FROM user WHERE id = ?",
        (user_id,)
    )

    # ยืนยันการลบ
    conn.commit()

    # โหลดข้อมูลใหม่
    load_data()

# =====================================
# ส่วนที่ 4: สร้างหน้าต่างหลัก
# =====================================

root = tk.Tk()
root.title("ระบบบันทึกข้อมูล")
root.geometry("500x400")


# =====================================
# ส่วนที่ 5: ตาราง Treeview
# =====================================

tree = ttk.Treeview(
    root,
    columns=("id", "name", "age"),
    show="headings",
    height=8
)

tree.heading("id", text="ID")
tree.heading("name", text="ชื่อ")
tree.heading("age", text="อายุ")

# ความกว้างคอลัมน์
tree.column("name", width=200, anchor="center")
tree.column("age", width=100, anchor="center")

tree.pack(pady=15)


# =====================================
# ส่วนที่ 6: Frame สำหรับฟอร์ม
# =====================================

form_frame = tk.Frame(root)
form_frame.pack(pady=10)


# =====================================
# ช่องกรอกชื่อ
# =====================================

lbl_name = tk.Label(
    form_frame,
    text="กรุณากรอกชื่อ:",
    font=("Arial", 12)
)

lbl_name.grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)


entry_name = tk.Entry(
    form_frame,
    font=("Arial", 12),
    width=25
)

entry_name.grid(
    row=0,
    column=1,
    columnspan=2,
    padx=5,
    pady=5,
    sticky="w"
)


# =====================================
# ช่องกรอกอายุ
# =====================================

lbl_age = tk.Label(
    form_frame,
    text="กรุณากรอกอายุ:",
    font=("Arial", 12)
)

lbl_age.grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)


entry_age = tk.Entry(
    form_frame,
    font=("Arial", 12),
    width=25
)

entry_age.grid(
    row=1,
    column=1,
    columnspan=2,
    padx=5,
    pady=5,
    sticky="w"
)


# =====================================
# ปุ่มบันทึกข้อมูล
# =====================================

btn_save = tk.Button(
    form_frame,
    text="บันทึก",
    font=("Arial", 12),
    width=10,
    command=save_data
)

btn_save.grid(
    row=2,
    column=1,
    padx=5,
    pady=10,
    sticky="w"
)


# =====================================
# ปุ่มโหลดข้อมูล
# =====================================

btn_load = tk.Button(
    form_frame,
    text="โหลดข้อมูล",
    font=("Arial", 12),
    width=10,
    command=load_data
)

btn_load.grid(
    row=2,
    column=2,
    padx=5,
    pady=10,
    sticky="w"
)


# =====================================
# ปุ่มลบข้อมูล
# =====================================

btn_Delete = tk.Button(
    form_frame,
    text="ลบ",
    font=("Arial", 12),
    width=10,
    command=delete_data
)

btn_Delete.grid(
    row=3,
    column=2,
    padx=5,
    pady=10,
    sticky="w"
)
# =====================================
# เริ่มต้นโปรแกรม
# =====================================

root.mainloop()


# ปิดการเชื่อมต่อ Database เมื่อปิดโปรแกรม
conn.close()