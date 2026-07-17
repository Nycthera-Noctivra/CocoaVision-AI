import streamlit as st
import cv2
import numpy as np

from detector import detect
from pdf_report import create_report

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="CocoaVision AI",
    page_icon="🌱",
    layout="wide"
)

# ===============================
# DATA INFORMASI
# ===============================

info = {

    "Buah Busuk": {
        "kategori":"Penyakit",
        "warna":"🔴",
        "deskripsi":"Buah mengalami pembusukan akibat infeksi jamur Phytophthora spp.",
        "solusi":"Pisahkan buah yang terinfeksi dan gunakan fungisida sesuai anjuran."
    },

    "Buah Sehat": {
        "kategori":"Normal",
        "warna":"🟢",
        "deskripsi":"Buah kakao berada dalam kondisi sehat.",
        "solusi":"Lakukan perawatan rutin."
    },

    "Kepik Penghisap": {
        "kategori":"Hama",
        "warna":"🟠",
        "deskripsi":"Kepik menghisap cairan buah sehingga muncul bercak hitam.",
        "solusi":"Lakukan sanitasi kebun dan pengendalian hama."
    },

    "Penggerek Buah": {
        "kategori":"Hama",
        "warna":"🟠",
        "deskripsi":"Larva menggerek bagian dalam buah sehingga merusak biji.",
        "solusi":"Musnahkan buah terserang dan lakukan pengendalian hama."
    }

}

# ===============================
# HEADER
# ===============================

with st.container():

    st.title("🌱 CocoaVision AI")

    st.caption("Implementasi Algoritma YOLOv8 untuk Deteksi Hama dan Penyakit pada Buah Kakao")

    st.divider()

# ===============================
# UPLOAD
# ===============================

with st.container():

    uploaded = st.file_uploader(
        "📤 Upload Gambar Buah Kakao",
        type=["jpg","jpeg","png"]
    )

# ===============================
# DETEKSI
# ===============================

if uploaded:

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    hasil, detections = detect(image)

    st.divider()

    col1, col2 = st.columns([1.15,0.85])

    # ==========================
    # HASIL GAMBAR
    # ==========================

    with col1:

        st.subheader("📷 Hasil Deteksi")

        st.image(
            cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    # ==========================
    # HASIL DETEKSI
    # ==========================

    with col2:

        st.subheader("📋 Informasi Deteksi")

        if len(detections)==0:

            st.error("Objek tidak ditemukan.")

        else:

            det = detections[0]

            nama = det["class"]

            conf = det["confidence"]

            cv2.imwrite(
            "hasil_deteksi.jpg",
            hasil
            )

            create_report(
            output_file="laporan_deteksi.pdf",
            image_path="hasil_deteksi.jpg",
            nama=nama,
            confidence=conf,
            kategori=info[nama]["kategori"],
            deskripsi=info[nama]["deskripsi"],
            solusi=info[nama]["solusi"]
            )

            st.success(f"{info[nama]['warna']} **{nama}**")

            st.metric(
                "Confidence",
                f"{conf*100:.2f}%"
            )

            st.progress(conf)

            st.info(f"Kategori : **{info[nama]['kategori']}**")

    # ==========================
    # DESKRIPSI
    # ==========================

    st.divider()

    st.subheader("📖 Deskripsi")

    st.write(info[nama]["deskripsi"])

    # ==========================
    # REKOMENDASI
    # ==========================

    st.subheader("✅ Rekomendasi Penanganan")

    st.success(info[nama]["solusi"])

    # ==========================
    # FOOTER
    # ==========================

    st.divider()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Model","YOLOv8")
    c2.metric("Confidence",f"{conf*100:.2f}%")
    c3.metric("Kategori",info[nama]["kategori"])
    c4.metric("Status","Deteksi Berhasil")

    st.divider()

    st.subheader("📄 Unduh Laporan")

    try:
        with open("laporan_deteksi.pdf", "rb") as pdf:

            st.download_button(
                label="📥 Download Laporan PDF",
                data=pdf,
                file_name="Laporan_Deteksi_Kakao.pdf",
                mime="application/pdf"
            )

    except FileNotFoundError:
        st.error("Laporan PDF belum berhasil dibuat.")