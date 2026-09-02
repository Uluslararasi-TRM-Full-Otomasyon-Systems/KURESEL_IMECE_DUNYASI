from pathlib import Path


ROOT_DOMAIN = "kureselsosyalimece.org.tr"
REDIRECT_DOMAIN = "kureselsosyalimece.com.tr"
STREAMLIT_APP_URL = "https://BURAYA_STREAMLIT_APP_URL_YAZIN.streamlit.app"
STREAMLIT_CNAME_TARGET = "BURAYA_STREAMLIT_CNAME_HEDEFINI_GIRIN"
STREAMLIT_APEX_TARGET = "BURAYA_STREAMLIT_ALIAS_VEYA_A_HEDEFINI_GIRIN"
STREAMLIT_A_TARGET = "BURAYA_STREAMLIT_A_KAYDI_IP_BILGISINI_GIRIN"


def dns_sablonu_uret() -> str:
    return f"""
KURESEL SOSYAL IMECE DUNYASI DNS AYAR SABLONU
=============================================

1. Streamlit Uygulama URL'si
   - Hedef uygulama: {STREAMLIT_APP_URL}

2. Ana domain icin kayit sablonu
   - Domain: {ROOT_DOMAIN}
   - Host: @
   - Yontem 1 (onerilen, destekleniyorsa): ALIAS / ANAME
     Deger: {STREAMLIT_APEX_TARGET}
   - Yontem 2 (Netlen sadece A kaydi istiyorsa):
     Deger: {STREAMLIT_A_TARGET}

3. WWW alt alan adi icin kayit sablonu
   - Domain: www.{ROOT_DOMAIN}
   - Kayit tipi: CNAME
   - Host: www
   - Deger: {STREAMLIT_CNAME_TARGET}

4. Yonlendirme sablonu
   - Domain: {REDIRECT_DOMAIN}
   - Kayit tipi: URL Redirect / Forwarding
   - Hedef: https://{ROOT_DOMAIN}
   - Durum kodu: 301 Permanent

5. Netlen paneline girmeden once doldurulacak alanlar
   - STREAMLIT_APP_URL
   - STREAMLIT_CNAME_TARGET
   - STREAMLIT_APEX_TARGET veya STREAMLIT_A_TARGET

Not:
   - Streamlit Cloud custom domain ekraninda verilen kayit degerlerini birebir kullanin.
   - Bu dosya yalnizca manuel panel girişi icin taslak uretir, DNS kaydini otomatik degistirmez.
""".strip()


def sablonu_kaydet():
    cikti_yolu = Path(__file__).with_name("dns_kayit_sablonu.txt")
    cikti_yolu.write_text(dns_sablonu_uret(), encoding="utf-8")
    print(f"DNS sablonu hazirlandi: {cikti_yolu}")


if __name__ == "__main__":
    print(dns_sablonu_uret())
    sablonu_kaydet()
