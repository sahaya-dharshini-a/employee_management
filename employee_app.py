import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
import csv
import re

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dc"
)
cursor = conn.cursor()

def show_total_employees():
    cursor.execute("SELECT COUNT(*) FROM Emp")
    total = cursor.fetchone()[0]
    messagebox.showinfo("Employee Count", f"Total Employees: {total}")
Button(root, text="Total Employees", command=show_total_employees).grid(row=13, column=2)

def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s",(username,password))
    if cursor.fetchone():
        messagebox.showinfo("Success","Login Successful")
        login_window.destroy()
        employee_management()
    else:
        messagebox.showerror("Error","Invalid Credentials")
def employee_count():
    cursor.execute("SELECT COUNT(*) FROM employee")
    total = cursor.fetchone()
    print("Total Employees:", total[0])

def toggle_password():
    entry_password.config(show='' if entry_password.cget('show')=='*' else '*')

def login_page():
    global login_window, entry_username, entry_password
    login_window = Tk()
    login_window.title("Login")

    Label(login_window,text="Username").grid(row=0,column=0)
    Label(login_window,text="Password").grid(row=1,column=0)

    entry_username = Entry(login_window)
    entry_password = Entry(login_window,show="*")

    entry_username.grid(row=0,column=1)
    entry_password.grid(row=1,column=1)

    Button(login_window,text="Login",command=login).grid(row=2,column=0,columnspan=2)
    Button(login_window,text="Show / Hide Password",command=toggle_password).grid(row=3,column=0,columnspan=2)
    login_window.mainloop()

def employee_management():
    def highlight_high_salary():
        cursor.execute("""
        SELECT e.EmpID, e.Name, e.Email, e.Age, d.DepartmentName, e.Salary
        FROM Emp e JOIN Department d ON e.DepartmentID=d.DepartmentID
        WHERE e.Salary > 50000
    """)
    rows = cursor.fetchall()
    listbox.delete(0, END)
    for row in rows:
        listbox.insert(END, row)
    Button(root, text="High Salary > 50k", command=highlight_high_salary).grid(row=16, column=0)

    def filter_by_salary():
        min_sal = entry_min_salary.get()
    max_sal = entry_max_salary.get()

    query = """
        SELECT e.EmpID, e.Name, e.Email, e.Age, d.DepartmentName, e.Salary
        FROM Emp e JOIN Department d ON e.DepartmentID=d.DepartmentID
        WHERE e.Salary BETWEEN %s AND %s
    """
    cursor.execute(query, (min_sal, max_sal))
    rows = cursor.fetchall()
    listbox.delete(0, END)
    for row in rows:
        listbox.insert(END, row)

    Label(root, text="Min Salary").grid(row=11, column=0)
entry_min_salary = Entry(root)
entry_min_salary.grid(row=11, column=1)

Label(root, text="Max Salary").grid(row=12, column=0)
entry_max_salary = Entry(root)
entry_max_salary.grid(row=12, column=1)

Button(root, text="Search by Salary", command=filter_by_salary).grid(row=13, column=0, columnspan=2)

    
    def clear_fields():
        entry_name.delete(0,END)
        entry_email.delete(0,END)
        entry_age.delete(0,END)
        entry_salary.delete(0,END)
        combo_dept.set('')

    def search_employee():
        name = input("Enter employee name: ")

    cursor.execute("SELECT * FROM employee WHERE name LIKE %s", ('%' + name + '%',))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    def add_employee():
        name,email,age,salary = entry_name.get(),entry_email.get(),entry_age.get(),entry_salary.get()
        dept = combo_dept.get()

        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            messagebox.showerror("Error","Invalid Email")
            return
        if salary < 10000:
            print("Salary must be above 10,000")
        return

        cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName=%s",(dept,))
        d=cursor.fetchone()
        if d:
            cursor.execute("INSERT INTO Emp(Name,Email,Age,DepartmentID,Salary) VALUES(%s,%s,%s,%s,%s)",
            (name,email,age,d[0],salary))
            conn.commit()
            fetch_data()
            clear_fields()
        else:
            messagebox.showerror("Error","Department not found")
    def show_employee_projects():
        selected = listbox.curselection()
    if selected:
        emp_id = listbox.get(selected)[0]
        cursor.execute("""
            SELECT p.ProjectName FROM Projects p
            JOIN EmployeeProject ep ON p.ProjectID=ep.ProjectID
            WHERE ep.EmpID=%s
        """, (emp_id,))
        rows = cursor.fetchall()
        projects = ", ".join([r[0] for r in rows]) if rows else "No Projects"
        messagebox.showinfo("Assigned Projects", projects)
    Button(root, text="View Projects", command=show_employee_projects).grid(row=16, column=1)

    def fetch_data():
        cursor.execute("""SELECT e.EmpID,e.Name,e.Email,e.Age,d.DepartmentName,e.Salary
                          FROM Emp e JOIN Department d ON e.DepartmentID=d.DepartmentID""")
        listbox.delete(0,END)
        for r in cursor.fetchall():
            listbox.insert(END,r)

    def export_csv():
        cursor.execute("SELECT Name,Email,Age,Salary FROM Emp")
        with open("employees.csv","w",newline="") as f:
            csv.writer(f).writerows(cursor.fetchall())
        messagebox.showinfo("Success","Exported to employees.csv")

    root=Tk()
    root.title("Employee Management")

    Label(root,text="Name").grid(row=0,column=0)
    entry_name=Entry(root); entry_name.grid(row=0,column=1)

    Label(root,text="Email").grid(row=1,column=0)
    entry_email=Entry(root); entry_email.grid(row=1,column=1)

    Label(root,text="Age").grid(row=2,column=0)
    entry_age=Entry(root); entry_age.grid(row=2,column=1)

    Label(root,text="Department").grid(row=3,column=0)
    combo_dept=ttk.Combobox(root,state="readonly"); combo_dept.grid(row=3,column=1)
    cursor.execute("SELECT DepartmentName FROM Department")
    combo_dept['values']=[r[0] for r in cursor.fetchall()]

    Label(root,text="Salary").grid(row=4,column=0)
    entry_salary=Entry(root); entry_salary.grid(row=4,column=1)

    Button(root,text="Add",command=add_employee).grid(row=5,column=0)
    Button(root,text="Export CSV",command=export_csv).grid(row=5,column=1)

    listbox=Listbox(root,width=70)
    listbox.grid(row=6,column=0,columnspan=2)

    fetch_data()
    root.mainloop()

login_page()
