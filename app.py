import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Simulasi EOQ & ROP", layout="centered")

st.title("📦 Simulasi EOQ (Economic Order Quantity) & ROP (Reorder Point)")

# Studi kasus
st.markdown("""
### 🧾 Studi Kasus:
Sebuah toko alat tulis menjual pulpen. Permintaan tahunan diperkirakan 1200 unit.
Setiap kali memesan, dikenakan biaya sebesar Rp 75.000.
Biaya penyimpanan per unit per tahun adalah Rp 2.500.
Waktu tunggu pengiriman (Lead Time) adalah 7 hari.

Berapa jumlah pemesanan optimal (EOQ) yang meminimalkan total biaya persediaan dan kapan harus melakukan pemesanan ulang (ROP)?
""")

# Rumus EOQ
st.markdown("""
### 📐 Rumus EOQ:
$$
EOQ = \\sqrt{\\frac{2DS}{H}}
$$
""")

# Rumus ROP
st.markdown("""
### 📐 Rumus ROP:
$$
ROP = \\text{Permintaan Harian} \\times \\text{Waktu Tunggu}
$$
""")

# Input variabel
D = st.number_input("Permintaan Tahunan (D)", value=1200.0, min_value=1.0, help="Jumlah total unit yang diminta dalam setahun.")
S = st.number_input("Biaya Pemesanan per Order (S)", value=75000.0, min_value=1.0, help="Biaya yang dikeluarkan setiap kali melakukan pemesanan.")
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2500.0, min_value=1.0, help="Biaya untuk menyimpan satu unit barang selama satu tahun.")
LT = st.number_input("Waktu Tunggu Pengiriman (Lead Time) dalam Hari", value=7.0, min_value=0.0, help="Jumlah hari yang dibutuhkan dari pemesanan hingga barang diterima.")

if D > 0 and S > 0 and H > 0:
    # Perhitungan EOQ
    EOQ = np.sqrt((2 * D * S) / H)

    st.success(f"📊 Jumlah pemesanan optimal (EOQ): {EOQ:.2f} unit")

    # Tampilkan proses perhitungan EOQ
    st.markdown("""
    ### 🔍 Proses Perhitungan EOQ:
    D = %.0f unit/tahun
    S = Rp %.0f per order
    H = Rp %.0f per unit/tahun

    $$
    EOQ = \\sqrt{\\frac{2 \\times %.0f \\times %.0f}{%.0f}} = \\sqrt{\\frac{%.0f}{%.0f}} = %.2f
    $$
    """ % (D, S, H, D, S, H, 2*D*S, H, EOQ))

    # Perhitungan ROP
    permintaan_harian = D / 365 # Asumsi 365 hari dalam setahun
    ROP = permintaan_harian * LT

    st.success(f"📈 Titik Pemesanan Ulang (ROP): {ROP:.2f} unit")

    # Tampilkan proses perhitungan ROP
    st.markdown("""
    ### 🔍 Proses Perhitungan ROP:
    Permintaan Tahunan (D) = %.0f unit/tahun
    Waktu Tunggu (Lead Time) = %.0f hari

    Permintaan Harian = D / 365 = %.0f / 365 = %.2f unit/hari

    $$
    ROP = \\text{Permintaan Harian} \\times \\text{Waktu Tunggu} = %.2f \\times %.0f = %.2f
    $$
    """ % (D, LT, D, permintaan_harian, permintaan_harian, LT, ROP))


    # Grafik total biaya
    # Pastikan Q memiliki nilai yang cukup untuk membuat grafik terlihat
    Q_min = max(1, int(EOQ * 0.5)) # Mulai dari 50% EOQ
    Q_max = int(EOQ * 2) # Sampai 200% EOQ
    Q = np.arange(Q_min, Q_max + 1) # Tambahkan 1 agar Q_max termasuk

    # Hindari pembagian dengan nol jika Q mengandung 0
    Q_filtered = Q[Q > 0]

    if len(Q_filtered) > 0:
        TC = (D / Q_filtered) * S + (Q_filtered / 2) * H

        fig, ax = plt.subplots(figsize=(8, 5)) # Ukuran grafik yang sedikit lebih besar
        ax.plot(Q_filtered, TC, label="Total Biaya", color='blue')
        ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
        ax.set_xlabel("Jumlah Pemesanan (Q)")
        ax.set_ylabel("Total Biaya (Rp)")
        ax.set_title("Grafik Total Biaya vs Jumlah Pemesanan")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7) # Tambahkan grid

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=600) # Ukuran gambar yang sedikit lebih besar

        st.markdown("""
        ### 📝 Penjelasan:
        - **Grafik Total Biaya:**
            - Titik minimum pada grafik menunjukkan jumlah pemesanan optimal (EOQ), di mana total biaya persediaan (biaya pemesanan + biaya penyimpanan) adalah yang terendah.
            - Di kiri EOQ: Terlalu sering memesan, menyebabkan biaya pemesanan tinggi.
            - Di kanan EOQ: Jumlah persediaan yang disimpan besar, menyebabkan biaya penyimpanan tinggi.
        - **EOQ (Economic Order Quantity):** Jumlah unit yang harus dipesan setiap kali untuk meminimalkan total biaya persediaan.
        - **ROP (Reorder Point):** Tingkat persediaan di mana pesanan baru harus ditempatkan untuk menghindari kehabisan stok selama waktu tunggu pengiriman.
        """)
    else:
        st.warning("Rentang jumlah pemesanan (Q) tidak valid untuk grafik. Sesuaikan nilai input.")

else:
    st.warning("Masukkan nilai D, S, dan H yang valid (semua harus > 0).")
