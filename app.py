import streamlit as st
from google import genai

# Kullanıcıdan anahtar istemek yerine gizli alandan otomatik alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("🛒 Akıllı E-Ticaret Yorum ve Analiz Paneli")
st.write("Yapay zeka destekli duygu analizi ve Gemini satın alma özeti asistanı.")

# Ürün adı girişi
urun_adi = st.text_input("Ürün Adı:", "Wayona Nylon Braided USB to Lightning Cable")

# Müşteri yorumları girişi
yorumlar_input = st.text_area(
    "Müşteri Yorumlarını Girin (Her satıra bir yorum):",
    "Ürün çok sağlam ve kaliteli.\nFiyata göre iyi ama biraz yavaş şarj ediyor.\nKesinlikle tavsiye ederim."
)

if st.button("Analiz Et ve Özet Çıkar"):
    if not yorumlar_input.strip():
        st.warning("Lütfen en az bir müşteri yorumu girin.")
    else:
        yorumlar_listesi = [y.strip() for y in yorumlar_input.split("\n") if y.strip()]
        
        prompt = f"""
        Aşağıda '{urun_adi}' adlı ürün için yapılmış müşteri yorumları verilmiştir. 
        Bu yorumları analiz ederek profesyonel bir "Gemini Satın Alma Özeti" çıkar. 
        Güçlü ve zayıf yönleri başlıklar altında maddeler halinde özetle.
        
        Yorumlar:
        {yorumlar_listesi}
        """
        
        with st.spinner("Yapay zeka yorumları analiz ediyor..."):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                st.subheader("📌 Gemini Satın Alma Özeti")
                st.write(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
