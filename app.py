import streamlit as st
from google import genai

# Sayfa ayarları
st.set_page_config(page_title="Akıllı E-Ticaret Analiz Paneli", page_icon="🛒", layout="centered")

# --- KUSURSUZ VE OKUNABİLİR ŞIK TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Genel Arka Planı Ferah Bir Beyaz Yapalım */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Şık Başlık Kutusu */
    .header-box {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(99, 102, 241,.3);
        margin-bottom: 25px;
    }
    .header-box h1 {
        color: white !important;
        font-size: 28px;
        margin-bottom: 10px;
    }
    .header-box p {
        color: #e0e7ff !important;
        font-size: 16px;
        margin: 0;
    }
    
    /* Etiketlerin (Label) Rengi ve Okunabilirliği */
    .stTextInput label, .stTextArea label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    /* Girdi Kutularını Beyaz ve Net Yapalım */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
    }
    
    /* Harika Mor/Mavi Buton */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# API anahtarını gizli alandan otomatik alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# --- ŞIK BAŞLIK KUTUSU ---
st.markdown("""
    <div class="header-box">
        <h1>🛒 Akıllı E-Ticaret Yorum ve Analiz Paneli</h1>
        <p>Yapay zeka destekli duygu analizi ve profesyonel satın alma özeti asistanı</p>
    </div>
""", unsafe_allow_html=True)

# Ürün adı girişi
urun_adi = st.text_input("📦 Ürün Adı:", "Wayona Nylon Braided USB to Lightning Cable")

# Müşteri yorumları girişi
yorumlar_input = st.text_area(
    "💬 Müşteri Yorumlarını Girin (Her satıra bir yorum):",
    "Ürün çok sağlam ve kaliteli.\nFiyata göre iyi ama biraz yavaş şarj ediyor.\nKesinlikle tavsiye ederim.",
    height=140
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Analiz Et ve Özet Çıkar"):
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
        
        with st.spinner("🤖 Yapay zeka yorumları titizlikle analiz ediyor..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Sonuç İçin Okunaklı Şık Kutu
                st.markdown(f"""
                <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h3 style="color: #4f46e5; margin-top: 0; margin-bottom: 15px; border-bottom: 2px solid #f3f4f6; padding-bottom: 10px;">📌 Gemini Satın Alma Özeti</h3>
                    <div style="color: #374151; font-size: 15px; line-height: 1.6;">
                        {response.text.replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {e}")

# Sol menü (Sidebar) şık görünüm
with st.sidebar:
    st.markdown("## ℹ️ Hakkında")
    st.info("Bu uygulama, e-ticaret yorumlarını yapay zeka ile analiz ederek güçlü ve zayıf yönleri hızlıca özetler.")
    st.markdown("---")
    st.markdown("🎓 **Proje Sunumu İçin Hazır**")
