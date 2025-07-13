import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="EOQ Calculator", layout="centered")
st.title("EOQ (Economic Order Quantity) Calculator")

st.latex(r"Rumus : EOQ = \sqrt{\frac{2DS}{H}}")
st.latex(r"D = \text{Permintaan tahunan (unit/tahun)}")
st.latex(r"S = \text{Biaya pemesanan per kali order}")
st.latex(r"H = \text{Biaya penyimpanan per unit per tahun}")

colD, colS, colH = st.columns(3)

with colD:
    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
with colS:
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
with colH:
    H = st.number_input("Biaya Penyimpanan per unit (H)", value=2.0)

if D > 0 and S > 0 and H > 0:
    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit")

    Q = np.arange(1, int(EOQ * 2))
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(Q, TC, label="Total Cost")
    ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
    ax.set_xlabel("Order Quantity")
    ax.set_ylabel("Total Cost")
    ax.set_title("EOQ vs Total Cost")
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.image(buf, width=480)

    st.markdown("### ✍️ Penjelasan:")
    st.markdown(f"""
    - Permintaan tahunan: **{D:.0f} unit**
    - Biaya pemesanan: **Rp {S:,.0f}**
    - Biaya penyimpanan: **Rp {H:,.0f} per unit**
    - Jadi, pemesanan optimal adalah **{EOQ:.2f} unit** setiap kali pesan.
    """)
else:
    st.warning("Masukkan nilai D, S, dan H yang valid (> 0).")
