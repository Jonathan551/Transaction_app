import tkinter as tk
from tkinter import messagebox
from db import connect_db
from admin_dashboard import AdminDashboard
from customer_dashboard import CustomerDashboard

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login Transfer Uang")
        master.geometry("300x200")

        tk.Label(master, text="Username").pack()
        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        tk.Label(master, text="Password").pack()
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        tk.Button(master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                SELECT u.username, r.nama_role FROM user u
                JOIN role r ON u.id_role = r.id_role
                WHERE u.username = %s AND u.password = %s
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                username, role = result  
                messagebox.showinfo("Login Berhasil", f"Halo {username}, Anda login sebagai {role}")

                self.master.destroy()
                dashboard = tk.Tk()

                if role == "Customer":
                    CustomerDashboard(dashboard, username)
                elif role in ["Admin", "Supervisor"]:
                    AdminDashboard(dashboard, username, role)
                else:
                    messagebox.showerror("Role Tidak Dikenali", f"Role '{role}' belum didukung.")

                dashboard.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal koneksi:\n{e}")


def main():
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
