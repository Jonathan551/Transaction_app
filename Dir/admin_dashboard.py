import tkinter as tk
from tkinter import messagebox, filedialog
from db import connect_db
import shutil
from fingerprint_verify import match_fingerprint
import os

class AdminDashboard:
    def __init__(self, master, username, role):
        self.master = master
        self.username = username
        self.role = role

        master.title(f"Dashboard {role}")
        master.geometry("500x500")

        tk.Label(master, text=f"Dashboard {role}", font=("Arial", 16)).pack(pady=10)

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack(pady=10)
        self.load_users()

        # Input dana
        tk.Label(master, text="Username Tujuan:").pack()
        self.entry_user = tk.Entry(master)
        self.entry_user.pack()

        tk.Label(master, text="Jumlah Dana:").pack()
        self.entry_amount = tk.Entry(master)
        self.entry_amount.pack()

        tk.Button(master, text="Tambahkan Dana", command=self.tambah_dana).pack(pady=10)
        if self.role == "Admin":
            tk.Button(master, text="Kelola Request Dana", command=self.kelola_request).pack(pady=5)
        tk.Button(master, text="Logout", command=self.logout, fg="white", bg="red").pack(pady=10)

        if self.role == "Supervisor":
            tk.Button(master, text="Tambah Fingerprint Admin", command=self.tambah_fingerprint_admin).pack(pady=5)
            tk.Button(master, text="Tambah User Baru", command=self.tambah_user).pack(pady=5)

    def load_users(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.username, s.saldo
                FROM user u
                LEFT JOIN saldo s ON u.id_user = s.id_user
            """)
            rows = cursor.fetchall()
            conn.close()

            self.listbox.delete(0, tk.END)
            for username, saldo in rows:
                saldo = saldo if saldo is not None else 0
                self.listbox.insert(tk.END, f"{username} - Saldo: Rp {saldo:,.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal load data:\n{e}")

    def tambah_dana(self):
        username = self.entry_user.get()
        try:
            jumlah = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Input Error", "Jumlah dana harus berupa angka.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_user FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "User tidak ditemukan.")
                return

            user_id = result[0]

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
                messagebox.showerror("Error", f"Gagal load request:\n{e}")

        def update_status(approved):
            try:
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("Pilih Request", "Silakan pilih request terlebih dahulu.")
                    return

                id_request = int(listbox.get(selection[0]).split()[1])

                conn = connect_db()
                cursor = conn.cursor()

                if approved:
                    fingerprint_file = filedialog.askopenfilename(title="Unggah Gambar Sidik Jari untuk Verifikasi")
                    if not fingerprint_file:
                        messagebox.showerror("Fingerprint Dibutuhkan", "Harap pilih file sidik jari Anda.")
                        return

                    # Verifikasi menggunakan file di folder 'fingerprints' berdasarkan username
                    cocok = match_fingerprint(fingerprint_file, self.username)


                    if not cocok:
                        messagebox.showerror("Verifikasi Gagal", "Sidik jari tidak cocok.")
                        return

                    # --- Jika fingerprint cocok, lanjut proses approve ---
                    cursor.execute("SELECT id_user, jumlah FROM request_topup WHERE id_request = %s", (id_request,))
                    user_id, jumlah = cursor.fetchone()

                    cursor.execute("SELECT id_user FROM saldo WHERE id_user = %s", (user_id,))
                    exists = cursor.fetchone()

                    if exists:
                        cursor.execute("UPDATE saldo SET saldo = saldo + %s WHERE id_user = %s", (jumlah, user_id))
                    else:
                        cursor.execute("INSERT INTO saldo (id_user, saldo) VALUES (%s, %s)", (user_id, jumlah))

                    cursor.execute("UPDATE request_topup SET status = 'Approved' WHERE id_request = %s", (id_request,))
                else:
                    cursor.execute("UPDATE request_topup SET status = 'Rejected' WHERE id_request = %s", (id_request,))

                conn.commit()
                conn.close()
                messagebox.showinfo("Sukses", "Status request diperbarui.")
                load_requests()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memperbarui status:\n{e}")

        frame = tk.Frame(win)
        frame.pack(pady=5)

        tk.Button(frame, text="✅ Setujui", command=lambda: update_status(True), width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="❌ Tolak", command=lambda: update_status(False), width=20).pack(side=tk.RIGHT, padx=10)

        load_requests()

    def tambah_fingerprint_admin(self):
        win = tk.Toplevel(self.master)
        win.title("Tambah Fingerprint Admin")
        win.geometry("400x200")

        tk.Label(win, text="Pilih Admin:").pack(pady=5)

        admin_var = tk.StringVar(win)
        dropdown = tk.OptionMenu(win, admin_var, "")
        dropdown.pack()

        def load_admins():
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT username FROM user
                    JOIN role ON user.id_role = role.id_role
                    WHERE role.nama_role = 'Admin'
                """)
                admins = [row[0] for row in cursor.fetchall()]
                menu = dropdown["menu"]
                menu.delete(0, "end")
                for name in admins:
                    menu.add_command(label=name, command=lambda v=name: admin_var.set(v))
                if admins:
                    admin_var.set(admins[0])
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat data admin: {e}")

        def simpan_fingerprint():
            target_user = admin_var.get()
            if not target_user:
                messagebox.showerror("Error", "Pilih admin terlebih dahulu.")
                return

            file_path = filedialog.askopenfilename(title="Pilih Gambar Sidik Jari")
            if not file_path:
                print("Tidak ada file yang dipilih.")
                return

            try:
                # Pastikan folder penyimpanan fingerprint ada
                base_dir = os.path.dirname(os.path.abspath(__file__))
                fingerprint_dir = os.path.join(base_dir, "fingerprints")
                os.makedirs(fingerprint_dir, exist_ok=True)

                file_name = f"{target_user}.png"
                dest_path = os.path.join(fingerprint_dir, file_name)

                print("📥 File asal:", file_path)
                print("📤 Akan disalin ke:", dest_path)

                shutil.copy(file_path, dest_path)

                # Simpan ke DB hanya id_user, tanpa file_path
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id_user FROM user WHERE username = %s", (target_user,))
                user_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO fingerprint (id_user) VALUES (%s)", (user_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", f"Fingerprint untuk {target_user} berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan fingerprint:\n{e}")
                print("❌ ERROR:", e)

        tk.Button(win, text="Unggah Fingerprint", command=simpan_fingerprint).pack(pady=10)
        load_admins()


    def tambah_user(self):
        win = tk.Toplevel(self.master)
        win.title("Tambah User Baru")
        win.geometry("350x300")

        tk.Label(win, text="Username:").pack()
        entry_username = tk.Entry(win)
        entry_username.pack()

        tk.Label(win, text="Password:").pack()
        entry_password = tk.Entry(win, show="*")
        entry_password.pack()

        tk.Label(win, text="Role:").pack()
        role_var = tk.StringVar()
        role_menu = tk.OptionMenu(win, role_var, "Customer", "Admin")
        role_menu.pack()
        role_var.set("Customer")  # default

        def simpan_user():
            username = entry_username.get()
            password = entry_password.get()
            role = role_var.get()

            if not username or not password:
                messagebox.showerror("Error", "Semua field wajib diisi.")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # Ambil id_role dari nama role
                cursor.execute("SELECT id_role FROM role WHERE nama_role = %s", (role,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", f"Role '{role}' tidak ditemukan di database.")
                    return

                id_role = result[0]

                # Masukkan user baru
                cursor.execute("""
                    INSERT INTO user (username, password, id_role)
                    VALUES (%s, %s, %s)
                """, (username, password, id_role))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", f"User '{username}' berhasil ditambahkan sebagai {role}.")
                win.destroy()
                self.load_users()  # reload saldo view
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambahkan user:\n{e}")

        tk.Button(win, text="Simpan", command=simpan_user).pack(pady=10)

    def logout(self):
        confirm = messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?")
        if confirm:
            self.master.destroy()
            import app
            app.main()