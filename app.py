import streamlit as st
from google import genai

# --- ŞIK TASARIM İÇİN CSS AYARLARI ---
st.set_page_config(page_title="Akıllı Analiz", page_icon="🛒", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    h1.main-title {
        color: #1e1e1e;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 3px solid #ff4b4b;
    }
    .stButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 15px !important;
    }
    .stButton > button:hover {
        background-color: #ff2b2b !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# API anahtarını gizli alandan otomatik alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Şık ortalanmış başlık
st.markdown('<h1 class="main-title">🛒 Akıllı E-Ticaret Yorum ve Analiz Paneli</h1>', unsafe_allow_html=True)
st.write("Yapay zeka destekli duygu analizi ve Gemini satın alma özeti asistanı.")

st.markdown("<br>", unsafe_allow_html=True)

# Ürün adı girişi
urun_adi = st.text_input("Ürün Adı:", "Wayona Nylon Braided USB to Lightning Cable")

# Müşteri yorumları girişi
yorumlar_input = st.text_area(
    "Müşteri Yorumlarını Girin (Her satıra bir yorum):",
    "Ürün çok sağlam ve kaliteli.\nFiyata göre iyi ama biraz yavaş şarj ediyor.\nKesinlikle tavsiye ederim.",
    height=150
)

if st.button("Analiz Et ve Özet Çıkar"):
    if not yorumlar_input.strip():
        st.warning("⚠️ Lütfen en az bir müşteri yorumu girin.")
    else:
        yorumlar_listesi = [y.strip() for y in yorumlar_input.split("\n") if y.strip()]
        
        prompt = f"""
        Aşağıda '{urun_adi}' adlı ürün için yapılmış müşteri yorumları verilmiştir. 
        Bu yorumları analiz ederek profesyonel bir "Gemini Satın Alma Özeti" çıkar. 
        Güçlü ve zayıf yönleri başlıklar altında maddeler halinde özetle.
        
        Yorumlar:
        {yorumlar_listesi}
        """
        
        with st.spinner("🤖 Yapay zeka yorumları analiz ediyor..."):
            try:
                # Güncel ve desteklenen model adı
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                st.markdown("---")
                st.subheader("📌 Gemini Satın Alma Özeti")
                
                # Şık sonuç kutusu
                st.markdown(f"""
                <div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border-left: 5px solid #2e7d32;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {e}")

# Sol menü (Sidebar)
with st.sidebar:
    st.markdown("## Hakkında")
    st.info("Bu uygulama, e-ticaret yorumlarını hızlıca analiz edip özetlemek için Google Gemini yapay zekasını kullanır.")
    st.markdown("---")
    st.write("🚀 Proje Sunumuna Hazır!")
