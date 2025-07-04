# admin_dashboard.py
import tkinter as tk
from tkinter import messagebox
from db import connect_db

class AdminDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Dashboard Admin")
        master.geometry("400x350")

   
        tk.Label(master, text="Dashboard Admin", font=("Arial", 16)).pack(pady=10)

    
        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack(pady=10)
        self.load_users()

      
        tk.Label(master, text="Username Tujuan:").pack()
        self.entry_user = tk.Entry(master)
        self.entry_user.pack()

        tk.Label(master, text="Jumlah Dana:").pack()
        self.entry_amount = tk.Entry(master)
        self.entry_amount.pack()

        tk.Button(master, text="Tambahkan Dana", command=self.tambah_dana).pack(pady=10)
        tk.Button(master, text="Kelola Request Dana", command=self.kelola_request).pack(pady=5)

    def load_users(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                SELECT u.username, s.saldo
                FROM user u
                LEFT JOIN saldo s ON u.id_user = s.id_user
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            self.listbox.delete(0, tk.END)
            for row in rows:
                saldo = row[1] if row[1] is not None else 0
                self.listbox.insert(tk.END, f"{row[0]} - Saldo: Rp {saldo:,.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal load data:\n{e}")

    def tambah_dana(self):
        username = self.entry_user.get()
        try:
            jumlah = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Input Error", "Jumlah dana harus angka.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Cari ID user
            cursor.execute("SELECT id_user FROM user WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            if not user_data:
                messagebox.showerror("Error", "User tidak ditemukan.")
                return

            user_id = user_data[0]


            cursor.execute("SELECT saldo FROM saldo WHERE id_user = %s", (user_id,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("UPDATE saldo SET saldo = saldo + %s WHERE id_user = %s", (jumlah, user_id))
            else:

                cursor.execute("INSERT INTO saldo (id_user, saldo) VALUES (%s, %s)", (user_id, jumlah))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", f"Dana sebesar Rp {jumlah:,.2f} berhasil ditambahkan ke {username}.")
            self.load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal tambah dana:\n{e}")

    def kelola_request(self):
        win = tk.Toplevel(self.master)
        win.title("Kelola Request Dana")
        win.geometry("500x300")

        listbox = tk.Listbox(win, width=70)
        listbox.pack(pady=10)

        def load_requests():
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.id_request, u.username, r.jumlah, r.status
                    FROM request_topup r
                    JOIN user u ON r.id_user = u.id_user
                    WHERE r.status = 'Pending'
                """)
                rows = cursor.fetchall()
                listbox.delete(0, tk.END)
                for row in rows:
                    listbox.insert(tk.END, f"ID {row[0]} | {row[1]} | Rp {row[2]:,.2f} | {row[3]}")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal load data:\n{e}")

        def update_status(approved):
            try:
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("Pilih Request", "Silakan pilih satu request terlebih dahulu.")
                    return
                selected_text = listbox.get(selection[0])
                id_request = int(selected_text.split()[1])  

                conn = connect_db()
                cursor = conn.cursor()

                if approved:
                    cursor.execute("SELECT id_user, jumlah FROM request_topup WHERE id_request = %s", (id_request,))
                    user_id, jumlah = cursor.fetchone()

               
                    cursor.execute("SELECT id_user FROM saldo WHERE id_user = %s", (user_id,))
                    exists = cursor.fetchone()
                    if exists:
                        cursor.execute("UPDATE saldo SET saldo = saldo + %s WHERE id_user = %s", (jumlah, user_id))
                    else:
                        cursor.execute("INSERT INTO saldo (id_user, saldo) VALUES (%s, %s)", (user_id, jumlah))

                    # Update status
                    cursor.execute("UPDATE request_topup SET status = 'Approved' WHERE id_request = %s", (id_request,))
                else:
                    cursor.execute("UPDATE request_topup SET status = 'Rejected' WHERE id_request = %s", (id_request,))

                conn.commit()
                conn.close()
                messagebox.showinfo("Sukses", "Status request berhasil diperbarui.")
                load_requests()
                self.load_users()  
            except Exception as e:
                messagebox.showerror("Error", f"Gagal proses request:\n{e}")

        # Tombol Approve / Reject
        frame = tk.Frame(win)
        frame.pack(pady=5)

        tk.Button(frame, text="✅ Setujui", command=lambda: update_status(True), width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="❌ Tolak", command=lambda: update_status(False), width=20).pack(side=tk.RIGHT, padx=10)

        load_requests()
