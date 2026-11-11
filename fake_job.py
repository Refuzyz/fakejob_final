import streamlit as st

# Fungsi yang akan memproses teks dari inputan pengguna di web
def deteksi_loker(teks_input, file_input):
    # Jika ada file/gambar yang diunggah, kita bisa mengasumsikan pengguna mengunggah screenshot.
    # Catatan: Untuk ekstraksi teks otomatis dari gambar (OCR), biasanya diperlukan library tambahan seperti pytesseract atau easyocr.
    # Di sini kita menyediakan form input teks dan media secara berdampingan.
    
    teks_untuk_dianalisis = teks_input
    catatan_tambahan = ""
    
    if file_input is not None:
        catatan_tambahan = "\n\n[Sistem mendeteksi adanya lampiran file/gambar. Analisis saat ini berfokus pada teks yang dimasukkan.]"

    if not teks_untuk_dianalisis.strip():
        if file_input is not None:
            return "File berhasil diunggah! Mohon salin/ketik teks penting yang ada di dalam gambar/dokumen tersebut ke kolom teks di atas untuk dianalisis oleh AI."
        return "Masukkan teks lowongan terlebih dahulu."

    # Ubah input pengguna jadi angka pakai vectorizer yang sama dengan saat training
    teks_vec = vectorizer.transform([teks_untuk_dianalisis])

    # AI memberikan tebakan (0 atau 1) dan persentase probabilitasnya
    hasil_prediksi = model.predict(teks_vec)[0]
    probabilitas = model.predict_proba(teks_vec)[0]

    prob_asli = probabilitas[0] * 100
    prob_palsu = probabilitas[1] * 100

    # Logika untuk menampilkan hasil ke layar web dengan alasan keyakinan
    if hasil_prediksi == 1:
        analisis = (
            f"⚠️ HATI-HATI! Loker ini terindikasi PALSU / PENIPUAN.\n\n"
            f"📊 Alasan Analisis Keyakinan AI:\n"
            f"- Probabilitas Palsu: {prob_palsu:.2f}% (Tinggi)\n"
            f"- Probabilitas Asli: {prob_asli:.2f}%\n\n"
            f"Sistem mendeteksi kecenderungan pola kalimat yang sering digunakan oleh penipu, "
            f"seperti meminta biaya pendaftaran, janji gaji tidak realistis, atau prosedur tidak resmi."
            f"{catatan_tambahan}"
        )
        return analisis
    else:
        analisis = (
            f"✅ AMAN. Loker ini terindikasi ASLI.\n\n"
            f"📊 Alasan Analisis Keyakinan AI:\n"
            f"- Probabilitas Asli: {prob_asli:.2f}% (Tinggi)\n"
            f"- Probabilitas Palsu: {prob_palsu:.2f}%\n\n"
            f"Sistem menilai struktur teks ini aman dan serupa dengan karakteristik penulisan lowongan kerja formal/profesional."
            f"{catatan_tambahan}"
        )
        return analisis

# Membuat kerangka website aplikasi dengan 2 input (teks dan file)
interface = gr.Interface(
    fn=deteksi_loker,
    inputs=[
        gr.Textbox(lines=5, placeholder="Paste teks lowongan di sini... (misal: syarat kerja, cara daftar, dll)", label="Teks Lowongan"),
        gr.File(label="Unggah Screenshot / File Lowongan (Opsional)")
    ],
    outputs=gr.Textbox(label="Hasil Analisis AI & Alasan Keyakinan"),
    title="Pendeteksi Loker Palsu (Anti-Scam) 🔎",
    description="Sistem Machine Learning untuk mendeteksi indikasi penipuan pada lowongan pekerjaan. Anda juga dapat mengunggah file atau tangkapan layar (screenshot) sebagai referensi tambahan."
)

# Menjalankan aplikasi web
interface.launch(server_name="0.0.0.0", server_port=10000)
