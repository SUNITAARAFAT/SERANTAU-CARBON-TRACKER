import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Serantau Carbon Tracker & Social Enterprise",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Mobile-Friendly & Clean Aesthetic
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f7f4;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 10px;
    }
    .fun-fact-card {
        background-color: #eef6fc;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #0288d1;
        margin-bottom: 15px;
    }
    .sdg-card {
        background-color: #fff9c4;
        border-radius: 10px;
        padding: 12px;
        border-left: 5px solid #fbc02d;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "fabric_logs" not in st.session_state:
    st.session_state.fabric_logs = pd.DataFrame([
        {
            "Tarikh": datetime.date.today().strftime("%Y-%m-%d"),
            "Ahli Kumpulan": "Sunita",
            "Bahan": "Denim",
            "Produk": "Pouch",
            "Berat (kg)": 1.20,
            "Kuantiti": 4,
            "Karbon Saved (kg CO2e)": 3.60,
            "Jarak Pemanduan (km)": 3.21
        },
        {
            "Tarikh": datetime.date.today().strftime("%Y-%m-%d"),
            "Ahli Kumpulan": "Nurul Saqinah",
            "Bahan": "Discarded PVC Banner",
            "Produk": "Tote Bag",
            "Berat (kg)": 2.50,
            "Kuantiti": 5,
            "Karbon Saved (kg CO2e)": 7.50,
            "Jarak Pemanduan (km)": 6.69
        },
        {
            "Tarikh": datetime.date.today().strftime("%Y-%m-%d"),
            "Ahli Kumpulan": "Nur Yasmin",
            "Bahan": "Songket / Batik",
            "Produk": "Pouch",
            "Berat (kg)": 0.80,
            "Kuantiti": 3,
            "Karbon Saved (kg CO2e)": 2.40,
            "Jarak Pemanduan (km)": 2.14
        }
    ])

if "sales_logs" not in st.session_state:
    st.session_state.sales_logs = pd.DataFrame([
        {
            "Tarikh": datetime.date.today().strftime("%Y-%m-%d"),
            "Ahli Kumpulan": "Sunita",
            "Produk": "Pouch",
            "Unit Terjual": 10,
            "Harga Seunit (RM)": 15.00,
            "Jumlah Jualan (RM)": 150.00
        },
        {
            "Tarikh": datetime.date.today().strftime("%Y-%m-%d"),
            "Ahli Kumpulan": "Nur Yasmin",
            "Produk": "Banner Tote Bag",
            "Unit Terjual": 8,
            "Harga Seunit (RM)": 30.00,
            "Jumlah Jualan (RM)": 240.00
        }
    ])

# Emission factor (approx. kg CO2e saved per kg upcycled fabric/material)
# Serantau baseline ratio: ~2,412.38 kg CO2e = 2,151 km driving (1 kg CO2e = 0.8918 km)
CO2_FACTOR = 3.0  # kg CO2e per kg material
KM_CONVERSION = 0.8918  # km vehicle driving per kg CO2e

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🌱 Serantau Carbon Tracker")
st.sidebar.caption("Inovasi Hijau & Upcycling Sisa Fabrik")

menu = st.sidebar.radio(
    "Pilih Modul / Menu:",
    ["📊 Visualisasi (Dashboard)", "📝 Rekod (Log Sisa & Upcycling)", "💼 Social Enterprise (Jualan)", "👥 Team Member (Jejak)", "🌍 SDG & Fun Facts"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Aplikasi Mesra Telefon**: Jalankan di pelayar web telefon pintar anda.")

# --- MODULE 1: DASHBOARD / VISUALISASI ---
if menu == "📊 Visualisasi (Dashboard)":
    st.title("📊 Visualisasi Impak Karbon & Upcycling")
    st.subheader("Impak Keseluruhan Program Jemari Lestari")

    # Metrics Calculation
    total_weight = st.session_state.fabric_logs["Berat (kg)"].sum()
    total_co2 = st.session_state.fabric_logs["Karbon Saved (kg CO2e)"].sum()
    total_km = st.session_state.fabric_logs["Jarak Pemanduan (km)"].sum()
    total_sales = st.session_state.sales_logs["Jumlah Jualan (RM)"].sum()
    total_items_sold = st.session_state.sales_logs["Unit Terjual"].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Pengurangan Karbon (kg CO2e)",
            value=f"{total_co2:,.2f} kg",
            delta="Penyelamatan Sisa"
        )
    with col2:
        st.metric(
            label="Setara Jarak Pemanduan",
            value=f"{total_km:,.1f} km",
            delta="Pemanduan Kenderaan"
        )
    with col3:
        st.metric(
            label="Jumlah Sisa Ditolak (Kg)",
            value=f"{total_weight:,.2f} kg",
            delta="Dari Tapak Pelupusan"
        )

    st.markdown("---")
    
    # Social Enterprise Summary Banner
    st.markdown(f"""
    <div class="metric-card">
        <h3>💼 Ringkasan Impak Enterprise Sosial</h3>
        <p><b>Jumlah Hasil Jualan:</b> RM {total_sales:,.2f} | <b>Jumlah Produk Terjual:</b> {total_items_sold} unit</p>
        <p><i>Setiap produk yang dijual menukarkan sisa fabrik/banner menjadi nilai ekonomi baharu untuk komuniti!</i></p>
    </div>
    """, unsafe_allow_html=True)

    # Charts / Breakdown
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.write("### 🧵 Sisa Fabrik Mengikut Bahan (kg)")
        material_df = st.session_state.fabric_logs.groupby("Bahan")["Berat (kg)"].sum()
        st.bar_chart(material_df)

    with col_chart2:
        st.write("### 🛍️ Jualan Mengikut Produk (RM)")
        sales_product_df = st.session_state.sales_logs.groupby("Produk")["Jumlah Jualan (RM)"].sum()
        st.bar_chart(sales_product_df)

# --- MODULE 2: REKOD (LOG SISA FABRIK) ---
elif menu == "📝 Rekod (Log Sisa & Upcycling)":
    st.title("📝 Rekod Pengumpulan & Upcycling Sisa")
    st.write("Masukkan maklumat sisa fabrik/banner yang diselamatkan dan dijadikan produk.")

    with st.form("log_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            member = st.selectbox("Ahli Kumpulan / Pembuat", ["Sunita", "Nurul Saqinah", "Nur Yasmin", "Ahli Komuniti / Murid"])
            material = st.selectbox("Jenis Bahan Sisa", ["Denim", "Songket / Batik", "Discarded PVC Banner", "Fabrik Campuran"])
            product = st.selectbox("Produk Terhasil", ["Pouch", "Tote Bag", "Custom Craft"])
        
        with col_f2:
            weight_grams = st.number_input("Berat Sisa Diberat (Gram)", min_value=10.0, max_value=50000.0, value=300.0, step=50.0)
            quantity = st.number_input("Kuantiti Produk Terhasil", min_value=1, max_value=500, value=1, step=1)
            entry_date = st.date_input("Tarikh Log", datetime.date.today())

        submit_log = st.form_submit_button("💾 Simpan Log Rekod")

        if submit_log:
            weight_kg = weight_grams / 1000.0
            co2_saved = weight_kg * CO2_FACTOR
            km_saved = co2_saved * KM_CONVERSION

            new_log = {
                "Tarikh": entry_date.strftime("%Y-%m-%d"),
                "Ahli Kumpulan": member,
                "Bahan": material,
                "Produk": product,
                "Berat (kg)": round(weight_kg, 2),
                "Kuantiti": quantity,
                "Karbon Saved (kg CO2e)": round(co2_saved, 2),
                "Jarak Pemanduan (km)": round(km_saved, 2)
            }
            
            st.session_state.fabric_logs = pd.concat([st.session_state.fabric_logs, pd.DataFrame([new_log])], ignore_index=True)
            st.success(f"✅ Berjaya merekod! {weight_kg:.2f} kg {material} telah diselamatkan = {co2_saved:.2f} kg CO2e dijimatkan.")

    st.write("### 📋 Jadual Log Rekod Sisa Fabrik")
    st.dataframe(st.session_state.fabric_logs, use_container_width=True)

# --- MODULE 3: SOCIAL ENTERPRISE (SALES TRACKER) ---
elif menu == "💼 Social Enterprise (Jualan)":
    st.title("💼 Enterprise Sosial: Rekod Jualan Produk Upcycling")
    st.write("Kira jualan pouch, tote bag banner, dan barangan barangan upcycled lain (Cipta Nilai).")

    with st.form("sales_form", clear_on_submit=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            seller = st.selectbox("Ahli Kumpulan / Wakil Jualan", ["Sunita", "Nurul Saqinah", "Nur Yasmin", "Pasukan Jualan Komuniti"])
            product_sold = st.selectbox("Jenis Produk Terjual", ["Pouch (Denim/Batik)", "Banner Tote Bag", "Aksesori Upcycled"])
        
        with col_s2:
            units_sold = st.number_input("Bilangan Unit Terjual", min_value=1, max_value=1000, value=5, step=1)
            unit_price = st.number_input("Harga Seunit (RM)", min_value=1.0, max_value=500.0, value=15.0, step=1.0)
            sale_date = st.date_input("Tarikh Jualan", datetime.date.today())

        submit_sale = st.form_submit_button("💰 Rekod Jualan")

        if submit_sale:
            total_rev = units_sold * unit_price
            new_sale = {
                "Tarikh": sale_date.strftime("%Y-%m-%d"),
                "Ahli Kumpulan": seller,
                "Produk": product_sold,
                "Unit Terjual": units_sold,
                "Harga Seunit (RM)": round(unit_price, 2),
                "Jumlah Jualan (RM)": round(total_rev, 2)
            }
            st.session_state.sales_logs = pd.concat([st.session_state.sales_logs, pd.DataFrame([new_sale])], ignore_index=True)
            st.success(f"🎉 Jualan Berjaya Direkod! {units_sold} unit {product_sold} = RM {total_rev:.2f}")

    st.write("### 📈 Jadual Rekod Jualan")
    st.dataframe(st.session_state.sales_logs, use_container_width=True)

# --- MODULE 4: TEAM MEMBER (JEJAK) ---
elif menu == "👥 Team Member (Jejak)":
    st.title("👥 Jejak Sumbangan Ahli Kumpulan")
    st.write("Pemantauan profil individu & kepimpinan dalam usaha kelestarian.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.write("### 🏆 Papan Pendahulu Upcycling (kg Sisa Diselamatkan)")
        team_weight = st.session_state.fabric_logs.groupby("Ahli Kumpulan")[["Berat (kg)", "Karbon Saved (kg CO2e)"]].sum().reset_index()
        st.dataframe(team_weight, use_container_width=True)

    with col_t2:
        st.write("### 💰 Papan Pendahulu Jualan (RM)")
        team_sales = st.session_state.sales_logs.groupby("Ahli Kumpulan")[["Unit Terjual", "Jumlah Jualan (RM)"]].sum().reset_index()
        st.dataframe(team_sales, use_container_width=True)

    st.markdown("---")
    st.write("### 🌟 Peranan Pasukan Teras Serantau Tracker")
    st.markdown("""
    - 👩‍💼 **Sunita**: *The Mastermind* - Perancang Strategi & Pembangunan Perniagaan.
    - 🧠 **Nurul Saqinah**: *The Thinker* - Pembangun Konsep & Model Pengiraan Karbon.
    - 🤝 **Nur Yasmin**: *The Connector* - Penggerak Komuniti & Rangkaian Jualan.
    """)

# --- MODULE 5: SDG & FUN FACTS ---
elif menu == "🌍 SDG & Fun Facts":
    st.title("🌍 Matlamat Pembangunan Mampan (SDG) & Fun Facts")

    st.subheader("📌 Penjajaran Matlamat SDG (UN Sustainable Development Goals)")
    
    col_sdg1, col_sdg2 = st.columns(2)
    with col_sdg1:
        st.markdown("""
        <div class="sdg-card">
            <h4>🌱 SDG 12: Responsible Consumption & Production</h4>
            <p>Melencongkan sisa tekstil dan banner PVC daripada dibuang ke tapak pelupusan sampah melalui kitar semula kreatif.</p>
        </div>
        <div class="sdg-card">
            <h4>☁️ SDG 13: Climate Action</h4>
            <p>Mengurangkan pelepasan gas rumah hijau (CO2e) secara berkesan melalui amalan sifar sisa.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_sdg2:
        st.markdown("""
        <div class="sdg-card">
            <h4>💼 SDG 8: Decent Work & Economic Growth</h4>
            <p>Memupuk kemahiran keusahawanan sosial dalam kalangan murid dan komuniti setempat.</p>
        </div>
        <div class="sdg-card">
            <h4>🌊 SDG 14: Life Below Water</h4>
            <p>Mencegah mikroplastik daripada fabrik sintetik daripada mencemari saliran dan laut.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💡 Tahukah Anda? (Fun Facts Sisa Fabrik & Banner)")

    st.markdown("""
    <div class="fun-fact-card">
        <h4>👖 Fakta Air & Denim (Jeans)</h4>
        <p>Tahukah anda? Penghasilan <b>sehelai seluar jeans denim</b> memerlukan anggaran <b>10,000 liter air</b>! Dengan merekod dan merawat semula perca denim menjadi pouch, anda membantu mengelakkan pembaziran sumber bumi.</p>
    </div>

    <div class="fun-fact-card">
        <h4>🪧 Fakta Banner PVC</h4>
        <p>Banner pengiklanan PVC mengambil masa sehingga <b>1,000 tahun untuk terurai</b> di tapak pelupusan! Mengubahnya menjadi tote bag kalis air memberikan jangka hayat kedua yang berguna.</p>
    </div>

    <div class="fun-fact-card">
        <h4>🩸 Fakta Mikroplastik & Kesihatan Laut</h4>
        <p>Kajian menunjukkan bahawa <b>80% sampel darah manusia</b> dikesan mengandungi mikroplastik akibat rantai sisa tidak terurus, dan lebih <b>300 spesies ikan laut</b> direkodkan menelan zarah plastik toksik.</p>
    </div>
    """, unsafe_allow_html=True)
