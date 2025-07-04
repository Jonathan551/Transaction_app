# 💸 Sistem Transfer Dana (Python + MySQL)

Aplikasi GUI berbasis Python dan Tkinter untuk sistem transfer dana sederhana antara pengguna, dengan dukungan login berbasis role (`Admin` / `Customer`) dan fitur top-up saldo serta request dana.

---

## 🛠️ Fitur Utama

### 👤 Login
- Autentikasi user berdasarkan database MySQL
- Role-based access (`Admin`, `Customer`)

### 👑 Dashboard Admin
- Melihat daftar user dan saldo mereka
- Menambahkan dana ke user
- Menyetujui atau menolak request top-up dari customer
- Verifikasi sidik jari (simulasi atau real device)

### 🙋 Dashboard Customer
- Melihat saldo milik sendiri
- Mengirim permintaan tambah dana (request top-up)

---

## 💽 Struktur Database (MySQL)

Nama database: `python_app`

### Tabel-tabel:
- `user` – Data user
- `role` – Role user (`Admin` / `Customer`)
- `saldo` – Saldo milik user
- `transaksi` – Catatan transfer dana
- `request_topup` – Request pengisian saldo oleh customer

```sql
CREATE TABLE request_topup (
    id_request INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT,
    jumlah DECIMAL(15,2) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    tanggal_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);
