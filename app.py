import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Simulasi EOQ", layout="wide")

st.title("Studi Kasus: EOQ (Economic Order Quantity)")

st.markdown("""
### 📋 Studi Kasus:
Sebuah toko alat tulis ingin menentukan jumlah pemesanan optimal (EOQ) untuk produk pulpen.

**Data yang diketahui:**
- Permintaan tahunan (D): 1.200 unit
- Biaya pemesanan per order (S): Rp 40.000
- Biaya penyimpanan per unit per tahun (H): Rp 2.000

EOQ digunakan untuk **meminimalkan total biaya persediaan**, yang terdiri dari biaya pemesanan dan biaya penyimpanan.

### 🧮 Rumus EOQ:
\[ EOQ = \sqrt{\frac{2DS}{H}} \]
""")

colD, colS, colH = st.columns([1, 1, 1])
with colD:
    D = st.number_input("Permintaan Tahunan (D)", value=1200.0)
with colS:
    S = st.number_input("Biaya Pemesanan per Order (S)", value=40000.0)
with colH:
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2000.0)

if D > 0 and S > 0 and H > 0:
    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"EOQ (Jumlah Pesan Optimal): {EOQ:.2f} unit")

    st.markdown("""
    ### 🔍 Proses Perhitungan:
    \[
    EOQ = \sqrt{\frac{2 \times %.0f \times %.0f}{%.0f}} = %.2f
    \]
    """ % (D, S, H, EOQ))

    Q = np.arange(1, int(EOQ * 2))
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(Q, TC, label="Total Biaya")
    ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
    ax.set_xlabel("Jumlah Pemesanan")
    ax.set_ylabel("Total Biaya (Rp)")
    ax.set_title("Grafik EOQ vs Total Biaya")
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.image(buf, width=600)

    st.markdown("""
    ### 📌 Interpretasi Grafik:
    - Kurva menunjukkan total biaya untuk berbagai jumlah pesanan.
    - Titik minimum adalah **EOQ**, di mana biaya total paling rendah.
    - Jika jumlah pesanan terlalu kecil atau terlalu besar, biaya akan naik.
    """)
else:
    st.warning("Masukkan nilai D, S, dan H yang valid (> 0).")
