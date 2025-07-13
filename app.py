import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Simulasi EOQ", layout="centered")

st.title("📦 Simulasi EOQ (Economic Order Quantity)")

# Studi kasus
st.markdown("""
### 🧾 Studi Kasus:
Sebuah toko alat tulis menjual pulpen. Permintaan tahunan diperkirakan 1200 unit. 
Setiap kali memesan, dikenakan biaya sebesar Rp 75.000. 
Biaya penyimpanan per unit per tahun adalah Rp 2.500. 

Berapa jumlah pemesanan optimal (EOQ) yang meminimalkan total biaya persediaan?
""")

# Rumus EOQ
st.markdown("""
### 📐 Rumus EOQ:
$$
EOQ = \sqrt{\frac{2DS}{H}}
$$
""")

# Input variabel
D = st.number_input("Permintaan Tahunan (D)", value=1200.0, min_value=1.0)
S = st.number_input("Biaya Pemesanan per Order (S)", value=75000.0, min_value=1.0)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2500.0, min_value=1.0)

if D > 0 and S > 0 and H > 0:
    # Perhitungan EOQ
    EOQ = np.sqrt((2 * D * S) / H)

    st.success(f"📊 Jumlah pemesanan optimal (EOQ): {EOQ:.2f} unit")

    # Tampilkan proses perhitungan
    st.markdown("""
    ### 🔍 Proses Perhitungan:
    D = %.0f unit/tahun  
    S = Rp %.0f per order  
    H = Rp %.0f per unit/tahun  

    $$
    EOQ = \sqrt{\frac{2 \times %.0f \times %.0f}{%.0f}} = \sqrt{\frac{%.0f}{%.0f}} = %.2f
    $$
    """ % (D, S, H, D, S, H, 2*D*S, H, EOQ))

    # Grafik total biaya
    Q = np.arange(1, int(EOQ*2))
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(Q, TC, label="Total Cost", color='blue')
    ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
    ax.set_xlabel("Jumlah Pemesanan (Q)")
    ax.set_ylabel("Total Biaya (Rp)")
    ax.set_title("Grafik Total Biaya vs Jumlah Pemesanan")
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.image(buf, width=480)

    st.markdown("""
    ### 📝 Penjelasan:
    - Titik minimum pada grafik menunjukkan jumlah pemesanan optimal (EOQ).
    - Di kiri EOQ: terlalu sering memesan, biaya pemesanan tinggi.
    - Di kanan EOQ: jumlah simpanan besar, biaya simpan tinggi.
    """)
else:
    st.warning("Masukkan nilai D, S, dan H yang valid (semua harus > 0).")