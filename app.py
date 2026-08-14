import streamlit as st
from google import genai

# Sayfa ayarları
st.set_page_config(page_title="Akıllı E-Ticaret Analiz Paneli", page_icon="🛒", layout="centered")

# --- ŞIK TASARIM İÇİN CSS KODLARI ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Üst Başlık Kutusu */
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
    
    /* Form Etiketleri */
    .stTextInput label, .stTextArea label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    /* Girdi Kutuları */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Şık Buton */
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

    /* Sonuç Kartları Tasarımı */
    .result-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .card-strong {
        background-color: #ecfdf5;
        border-left: 6px solid #10b981;
        border: 1px solid #d1fae5;
    }
    .card-weak {
        background-color: #fff1f2;
        border-left: 6px solid #f43f5e;
        border: 1px solid #ffe4e6;
    }
    .card-summary {
        background-color: #eff6ff;
        border-left: 6px solid #3b82f6;
        border: 1px solid #dbeafe;
    }
    </style>
""", unsafe_allow_html=True)

# API anahtarını gizli alandan otomatik alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Şık Başlık
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
        
        # Yapay zekadan net bölümler halinde çıktı almasını isteyelim
        prompt = f"""
        Aşağıda '{urun_adi}' adlı ürün için yapılmış müşteri yorumları verilmiştir. 
        Bu yorumları analiz et ve tam olarak şu 3 başlık altında yanıt ver (başlık isimlerini değiştirme):

        ### GİRİŞ
        (Genel bir değerlendirme cümlesi yaz)

        ### GÜÇLÜ YÖNLER
        (Maddeler halinde güçlü yönleri yaz)

        ### ZAYIF YÖNLER
        (Maddeler halinde zayıf yönleri yaz)

        ### GENEL KARAR
        (Sonuç ve satın alma tavsiyesi kararını yaz)

        Yorumlar:
        {yorumlar_listesi}
        """
        
        with st.spinner("🤖 Yapay zeka yorumları titizlikle analiz ediyor..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                
                text = response.text
                
                # Çıktıyı başlıklara göre akıllıca ayıralım
                parts = {}
                current_key = "GİRİŞ"
                for line in text.split('\n'):
                    if "GÜÇLÜ YÖNLER" in line.upper():
                        current_key = "GÜÇLÜ YÖNLER"
                        continue
                    elif "ZAYIF YÖNLER" in line.upper():
                        current_key = "ZAYIF YÖNLER"
                        continue
                    elif "GENEL KARAR" in line.upper():
                        current_key = "GENEL KARAR"
                        continue
                    
                    parts.setdefault(current_key, []).append(line)
                
                giris_text = "\n".join(parts.get("GİRİŞ", [])).strip()
                guclu_text = "\n".join(parts.get("GÜÇLÜ YÖNLER", [])).strip()
                zayif_text = "\n".join(parts.get("ZAYIF YÖNLER", [])).strip()
                 karar_text = "\n".join(parts.get("GENEL KARAR", [])).strip()

                st.markdown("---")
                st.subheader("📌 Gemini Satın Alma Analiz Raporu")
                
                if giris_text:
                    st.write(giris_text)
                    st.markdown("<br>", unsafe_allow_html=True)

                # 1. GÜÇLÜ YÖNLER KUTUSU (Yeşil Tema)
                if guclu_text:
                    st.markdown(f"""
                    <div class="result-card card-strong">
                        <h4 style="color: #065f46; margin-top: 0; margin-bottom: 10px;">💪 Güçlü Yönler</h4>
                        <div style="color: #064e3b; font-size: 15px; line-height: 1.6;">
                            {guclu_text.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 2. ZAYIF YÖNLER KUTUSU (Kırmızı/Pembe Tema)
                if zayif_text:
                    st.markdown(f"""
                    <div class="result-card card-weak">
                        <h4 style="color: #9f1239; margin-top: 0; margin-bottom: 10px;">⚠️ Zayıf Yönler / Eksikler</h4>
                        <div style="color: #881337; font-size: 15px; line-height: 1.6;">
                            {zayif_text.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 3. GENEL KARAR KUTUSU (Mavi Tema)
                if karar_text:
                    st.markdown(f"""
                    <div class="result-card card-summary">
                        <h4 style="color: #1e40af; margin-top: 0; margin-bottom: 10px;">🎯 Genel Karar ve Tavsiye</h4>
                        <div style="color: #1e3a8a; font-size: 15px; line-height: 1.6;">
                            {karar_text.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {e}")

# Sol menü (Sidebar)
with st.sidebar:
    st.markdown("## ℹ️ Hakkında")
    st.info("Bu uygulama, e-ticaret yorumlarını yapay zeka ile analiz ederek güçlü ve zayıf yönleri hızlıca özetler.")
    st.markdown("---")
    st.markdown("🎓 **Proje Sunumuna Hazır!**")
