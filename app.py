import streamlit as st
import pandas as pd
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Akıllı E-Ticaret Asistanı", layout="centered")

st.title("🛒 Akıllı E-Ticaret Yorum ve Analiz Paneli")
st.write("Yapay zeka destekli duygu analizi ve Gemini satın alma özeti asistanı.")

# API Anahtarı girişi
api_key = st.text_input("Gemini API Anahtarınızı Girin:", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Kullanıcıdan veri alma
        urun_adi = st.text_input("Ürün Adı:", "Wayona Nylon Braided USB to Lightning Cable")
        yorumlar_input = st.text_area("Müşteri Yorumlarını Girin (Her satıra bir yorum):", 
                                      "Ürün çok sağlam ve kaliteli.\nFiyatına göre iyi ama biraz yavaş şarj ediyor.\nKesinlikle tavsiye ederim.")

        if st.button("Analiz Et ve Özet Çıkar"):
            if yorumlar_input:
                with st.spinner("Gemini yorumları analiz ediyor..."):
                    prompt = f"'{urun_adi}' ürünü için şu müşteri yorumlarını analiz ederek güçlü ve zayıf yönlerini maddeler halinde özetle:\n{yorumlar_input}"
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=prompt,
                    )
                    
                    st.subheader("📌 Gemini Satın Alma Özeti")
                    st.write(response.text)
            else:
                st.warning("Lütfen analiz için birkaç yorum girin.")
    except Exception as e:
        st.error(e)
else:
    st.info("Devam etmek için lütfen Gemini API anahtarınızı girin.")
