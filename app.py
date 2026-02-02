from flask import Flask, render_template, request, redirect, send_file, flash
import mysql.connector
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'alya_secret_key'

# Konfigurasi Database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'klinik_alya'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- ROUTE DASHBOARD (READ RAWAT INAP) ---
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT ri.id_rawat, p.nama, k.id_kamar, k.harga, ri.tgl_masuk, ri.tgl_keluar
        FROM rawat_inap_alya ri
        JOIN pasien_alya p ON ri.id_pasien = p.id_pasien
        JOIN kamar_alya k ON ri.id_kamar = k.id_kamar
    """
    cursor.execute(query)
    data_rawat = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', data_rawat=data_rawat)


# --- ROUTE PROSES BAYAR (CREATE TRANSAKSI) ---
@app.route('/bayar/<id_rawat>')
def proses_bayar(id_rawat):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil data untuk hitung biaya
    cursor.execute("""
        SELECT ri.*, k.harga 
        FROM rawat_inap_alya ri 
        JOIN kamar_alya k ON ri.id_kamar = k.id_kamar 
        WHERE ri.id_rawat = %s""", (id_rawat,))
    row = cursor.fetchone()
    
    if row:
        # Hitung selisih hari
        selisih = row['tgl_keluar'] - row['tgl_masuk']
        durasi = max(selisih.days, 1) # Minimal 1 hari
        total_biaya = durasi * row['harga']
        tgl_skrg = datetime.now().strftime('%Y-%m-%d')
        
        # Insert ke tabel transaksi
        sql = "INSERT INTO transaksi_alya (id_pasien, total_biaya, status_pembayaran, tgl) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (row['id_pasien'], total_biaya, 1, tgl_skrg))
        conn.commit()
        flash(f"Transaksi Berhasil! Total Biaya: Rp {total_biaya:,.0f}")
    
    cursor.close()
    conn.close()
    return redirect('/transaksi')

# --- ROUTE LIST TRANSAKSI (READ CRUD) ---
@app.route('/transaksi')
def list_transaksi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.id_transaksi, t.id_pasien, p.nama, t.total_biaya, t.status_pembayaran, t.tgl
        FROM transaksi_alya t
        JOIN pasien_alya p ON t.id_pasien = p.id_pasien
        ORDER BY t.id_transaksi ASC
    """
    cursor.execute(query)
    data_transaksi = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('transaksi.html', data_transaksi=data_transaksi)

# --- ROUTE UPDATE STATUS (UPDATE CRUD) ---
@app.route('/transaksi/update/<int:id_transaksi>')
def update_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Cek status sekarang
    cursor.execute("SELECT status_pembayaran FROM transaksi_alya WHERE id_transaksi = %s", (id_transaksi,))
    current = cursor.fetchone()
    if current is not None:
        new_status = 0 if current['status_pembayaran'] else 1
        cursor.execute("UPDATE transaksi_alya SET status_pembayaran = %s WHERE id_transaksi = %s", (new_status, id_transaksi))
        conn.commit()
        flash("Status pembayaran diperbarui.")
    cursor.close()
    conn.close()
    return redirect('/transaksi')

# --- ROUTE DELETE (DELETE CRUD) ---
@app.route('/transaksi/delete/<int:id_transaksi>')
def delete_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi_alya WHERE id_transaksi = %s", (id_transaksi,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Data transaksi dihapus.")
    return redirect('/transaksi')

# --- ROUTE EDIT TRANSAKSI (UPDATE DATA) ---
@app.route('/transaksi/edit/<int:id_transaksi>', methods=['GET', 'POST'])
def edit_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        total_biaya = request.form['total_biaya']
        tgl = request.form['tgl']
        status_pembayaran = request.form['status_pembayaran']
        cursor.execute(
            "UPDATE transaksi_alya SET total_biaya=%s, tgl=%s, status_pembayaran=%s WHERE id_transaksi=%s",
            (total_biaya, tgl, status_pembayaran, id_transaksi)
        )
        conn.commit()
        flash("Data transaksi berhasil diubah.")
        cursor.close()
        conn.close()
        return redirect('/transaksi')
    else:
        cursor.execute("SELECT t.*, p.nama FROM transaksi_alya t JOIN pasien_alya p ON t.id_pasien = p.id_pasien WHERE t.id_transaksi=%s", (id_transaksi,))
        transaksi = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_transaksi.html', transaksi=transaksi)

# --- ROUTE TAMBAH TRANSAKSI (CREATE DATA) ---
@app.route('/transaksi/tambah', methods=['GET', 'POST'])
def tambah_transaksi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_pasien = request.form['id_pasien']
        total_biaya = request.form['total_biaya']
        status_pembayaran = request.form['status_pembayaran']
        tgl = request.form['tgl']

        cursor.execute("""
            INSERT INTO transaksi_alya (id_pasien, total_biaya, status_pembayaran, tgl)
            VALUES (%s, %s, %s, %s)
        """, (id_pasien, total_biaya, status_pembayaran, tgl))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Data transaksi berhasil ditambahkan.")
        return redirect('/transaksi')

    # Ambil data pasien untuk dropdown
    cursor.execute("SELECT * FROM pasien_alya")
    pasien = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('tambah_transaksi.html', pasien=pasien)



# DATA PASIEN
@app.route("/pasien")
def pasien():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pasien_alya")
    data = cursor.fetchall()
    return render_template("pasien.html", pasien=data)

# CETAK PDF PASIEN
@app.route("/cetak_pasien")
def cetak_pasien():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien, nama FROM pasien_alya")
    data = cursor.fetchall()

    class PDF(FPDF):
        def header(self):
            self.set_font('DejaVu', '', 16)
            self.set_text_color(30, 64, 175)
            self.cell(0, 10, "Laporan Data Pasien", ln=True, align='C')
            self.ln(2)
            self.set_draw_color(30, 64, 175)
            self.set_line_width(1)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font('DejaVu', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    pdf = PDF()
    # Tambahkan font SEBELUM add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.add_page()
    # Table header
    pdf.set_fill_color(30, 64, 175)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 10, "ID Pasien", border=1, align='C', fill=True)
    pdf.cell(120, 10, "Nama Pasien", border=1, align='C', fill=True)
    pdf.ln()
    # Table body
    pdf.set_text_color(0, 0, 0)
    for row in data:
        pdf.cell(40, 10, str(row['id_pasien']), border=1, align='C')
        pdf.cell(120, 10, row['nama'], border=1)
        pdf.ln()
    pdf_path = "laporan_pasien.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)




@app.route("/cetak_transaksi")
def cetak_transaksi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.id_transaksi, t.id_pasien, p.nama, t.total_biaya, t.status_pembayaran, t.tgl
        FROM transaksi_alya t
        JOIN pasien_alya p ON t.id_pasien = p.id_pasien
        ORDER BY t.id_transaksi ASC
    """
    cursor.execute(query)
    data_transaksi = cursor.fetchall()

    class PDF(FPDF):
        def header(self):
            self.set_font('DejaVu', '', 16)
            self.set_text_color(30, 64, 175)
            self.cell(0, 10, "Laporan Data Transaksi", ln=True, align='C')
            self.ln(2)
            self.set_draw_color(30, 64, 175)
            self.set_line_width(1)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font('DejaVu', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    pdf = PDF()
    # Tambahkan font SEBELUM add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.add_page()
    # Table header
    pdf.set_fill_color(30, 64, 175)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 10, "ID Transaksi", border=1, align='C', fill=True)
    pdf.cell(60, 10, "Nama Pasien", border=1, align='C', fill=True)
    pdf.cell(30, 10, "Total Bayar", border=1, align='C', fill=True)
    pdf.cell(30, 10, "Tanggal", border=1, align='C', fill=True)
    pdf.cell(30, 10, "Status", border=1, align='C', fill=True)
    pdf.ln()
    # Table body
    pdf.set_text_color(0, 0, 0)
    for row in data_transaksi:
        status = "LUNAS" if row['status_pembayaran'] == 1 else "BELUM"
        total = f"Rp {row['total_biaya']:,.0f}"

        pdf.cell(40, 10, str(row['id_transaksi']), border=1, align='C')
        pdf.cell(60, 10, row['nama'], border=1)
        pdf.cell(30, 10, total, border=1)
        pdf.cell(30, 10, str(row['tgl']), border=1, align='C')
        pdf.cell(30, 10, status, border=1)
        pdf.ln()
    pdf_path = "laporan_Transaksi.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)