# customer_dashboard.py
import tkinter as tk
from tkinter import messagebox
from db import connect_db

class CustomerDashboard:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Dashboard Customer")
        master.geometry("350x250")

        tk.Label(master, text=f"Halo, {username}", font=("Arial", 14)).pack(pady=10)

        self.saldo_var = tk.StringVar()
        self.label_saldo = tk.Label(master, textvariable=self.saldo_var, font=("Arial", 12))
        self.label_saldo.pack(pady=5)

        self.load_saldo()

        # Form request dana
        tk.Label(master, text="Jumlah dana yang diminta:").pack()
        self.entry_jumlah = tk.Entry(master)
        self.entry_jumlah.pack()

        tk.Button(master, text="Request Tambah Dana", command=self.request_topup).pack(pady=10)
        tk.Button(master, text="Logout", command=self.logout, fg="white", bg="red").pack(pady=10)

    def load_saldo(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                SELECT s.saldo FROM user u
                JOIN saldo s ON u.id_user = s.id_user
                WHERE u.username = %s
            """
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.saldo_var.set(f"Saldo Anda: Rp {result[0]:,.2f}")
            else:
                self.saldo_var.set("Saldo Anda: Rp 0.00")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal load saldo:\n{e}")

    def request_topup(self):
        try:
            jumlah = float(self.entry_jumlah.get())
        except ValueError:
            messagebox.showerror("Input Error", "Jumlah harus berupa angka.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT id_user FROM user WHERE username = %s", (self.username,))
            user = cursor.fetchone()

            if not user:
                messagebox.showerror("Error", "User tidak ditemukan.")
                return

            id_user = user[0]

            cursor.execute("INSERT INTO request_topup (id_user, jumlah) VALUES (%s, %s)", (id_user, jumlah))
            conn.commit()
            conn.close()

            messagebox.showinfo("Berhasil", "Permintaan tambah dana telah dikirim dan menunggu persetujuan admin.")
            self.entry_jumlah.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengirim permintaan:\n{e}")

    def logout(self):
        confirm = messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?")
        if confirm:
            self.master.destroy()
            import app
            app.main()
