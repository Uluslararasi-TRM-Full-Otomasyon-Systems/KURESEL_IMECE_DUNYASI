#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Küresel İmece Dünyası Yönetim Paneli - Geliştirilmiş Canlı Sürüm (Streamlit)
"""

import os
import sys
import json
import logging
from datetime import datetime
import streamlit as st
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KureselImeceDunyasiPanel:
    def __init__(self):
        self.version = "3.0"
        self.status = "ACTIVE"
        self.target = "magazanolsun.com"
        self.products_file = "toplanan_urunler.json"
    
    def load_products(self):
        """Ürünleri JSON dosyasından yükle"""
        try:
            if os.path.exists(self.products_file):
                with open(self.products_file, 'r', encoding='utf-8') as f:
                    products = json.load(f)
                return products
            else:
                return []
        except Exception as e:
            logger.error(f"Ürün yükleme hatası: {e}")
            return []

    def start_panel(self):
        st.set_page_config(page_title="KÜRESEL İMECE DÜNYASI", page_icon="🌍")
        
        st.title("🌍 KÜRESEL İMECE DÜNYASI v3.0")
        st.subheader("Dijital Çağın Üretim Kooperatifi & Sınırsız İstihdam Modeli")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Durum", value=self.status, delta="AKTİF")
        with col2:
            st.metric(label="Sürüm", value=self.version)
        with col3:
            st.metric(label="Hedef", value=self.target)
        
        st.markdown("---")
        st.success("✅ Full Automation System | AI Powered | 7/24 Active")
        st.info("📍 Cloud modu aktif")
        st.info("⏰ Gerçek zamanlı sistem takibi başlatıldı...")
        
        # Ürün Tablosu Bölümü
        st.markdown("---")
        st.header("📦 Depodaki Ürünler")
        
        products = self.load_products()
        
        if products:
            # DataFrame oluştur
            df = pd.DataFrame(products)
            
            # Sadece önemli sütunları göster
            display_columns = ['urun_adi', 'fiyat', 'firma', 'toplanma_tarihi']
            df_display = df[display_columns].copy()
            
            # Sütun adlarını Türkçeleştir
            df_display.columns = ['Ürün Adı', 'Fiyat (TL)', 'Firma', 'Toplanma Tarihi']
            
            # Fiyat sütununu formatla
            df_display['Fiyat (TL)'] = df_display['Fiyat (TL)'].apply(lambda x: f"{x} TL" if x else "-")
            
            # Tarihi formatla
            df_display['Toplanma Tarihi'] = pd.to_datetime(df_display['Toplanma Tarihi']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Tabloyu göster
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # İstatistikler
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Ürün", len(products))
            with col2:
                avg_price = df['fiyat'].apply(lambda x: float(x) if x and str(x).replace('.', '').replace(',', '').isdigit() else 0).mean()
                st.metric("Ortalama Fiyat", f"{avg_price:.2f} TL" if avg_price > 0 else "-")
            with col3:
                st.metric("Son Güncelleme", df_display['Toplanma Tarihi'].iloc[0] if len(df_display) > 0 else "-")
            
            # Detaylı görünüm seçeneği
            with st.expander("📋 Detaylı Ürün Bilgileri"):
                for i, product in enumerate(products):
                    st.markdown(f"**{i+1}. {product['urun_adi']}**")
                    st.markdown(f"- Fiyat: {product['fiyat']} TL")
                    st.markdown(f"- Firma: {product['firma']}")
                    st.markdown(f"- Açıklama: {product['aciklama']}")
                    st.markdown(f"- Link: [{product['urun_linki']}]({product['urun_linki']})")
                    st.markdown("---")
        else:
            st.warning("⚠️ Depoda henüz ürün bulunmuyor. Ürün çekme operasyonu başlatın.")

if __name__ == "__main__":
    try:
        panel = KureselImeceDunyasiPanel()
        panel.start_panel()
        logger.info("✅ Yönetim paneli arayüzü başarıyla ayağa kalktı.")
    except Exception as e:
        logger.error(f"❌ Panel başlatma hatası: {e}")
        st.error(f"❌ Panel başlatma hatası: {e}")
        sys.exit(1)
