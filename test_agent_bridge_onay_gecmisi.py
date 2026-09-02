#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
agent_bridge.py onay_gecmisi fonksiyonu test scripti
Dosya yoksa boş liste döndürme mantığını test eder
"""

import os
import json
from agent_bridge import AgentBridge

def test_onay_gecmisi_bos_dosya():
    """Dosya yoksa boş liste döndürme testi"""
    print("Test 1: Dosya yoksa boş liste döndürme")
    print("-" * 50)
    
    # Test için geçici dosya adı
    test_dosyasi = "test_sozlesme_onaylari.json"
    
    # Dosyayı sil (varsa)
    if os.path.exists(test_dosyasi):
        os.remove(test_dosyasi)
    
    # Bridge oluştur ve test dosyasını kullan
    bridge = AgentBridge()
    bridge.onay_dosyasi = test_dosyasi
    
    # onay_gecmisi çağır
    sonuc = bridge.onay_gecmisi()
    
    print(f"Sonuç: {json.dumps(sonuc, indent=2, ensure_ascii=False)}")
    
    # Beklenen sonuç kontrolü
    beklenen = {
        "durum": "ebasarili",
        "toplam_onay": 0,
        "onaylar": []
    }
    
    if sonuc == beklenen:
        print("✅ Test BAŞARILI: Dosya yoksa doğru format döndürüldü")
    else:
        print("❌ Test BAŞARISIZ: Beklenen sonuç alınamadı")
        print(f"Beklenen: {beklenen}")
        print(f"Alınan: {sonuc}")
    
    # Temizlik
    if os.path.exists(test_dosyasi):
        os.remove(test_dosyasi)
    
    print()

def test_onay_gecmisi_bos_dosya_json():
    """Boş JSON dosyası testi"""
    print("Test 2: Boş JSON dosyası testi")
    print("-" * 50)
    
    test_dosyasi = "test_sozlesme_onaylari.json"
    
    # Boş JSON dosyası oluştur
    with open(test_dosyasi, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    
    # Bridge oluştur
    bridge = AgentBridge()
    bridge.onay_dosyasi = test_dosyasi
    
    # onay_gecmisi çağır
    sonuc = bridge.onay_gecmisi()
    
    print(f"Sonuç: {json.dumps(sonuc, indent=2, ensure_ascii=False)}")
    
    # Beklenen sonuç kontrolü
    beklenen = {
        "durum": "ebasarili",
        "toplam_onay": 0,
        "onaylar": []
    }
    
    if sonuc == beklenen:
        print("✅ Test BAŞARILI: Boş dosya için doğru format döndürüldü")
    else:
        print("❌ Test BAŞARISIZ: Beklenen sonuç alınamadı")
        print(f"Beklenen: {beklenen}")
        print(f"Alınan: {sonuc}")
    
    # Temizlik
    if os.path.exists(test_dosyasi):
        os.remove(test_dosyasi)
    
    print()

def test_onay_gecmisi_verili_dosya():
    """Verili dosya testi"""
    print("Test 3: Verili dosya testi")
    print("-" * 50)
    
    test_dosyasi = "test_sozlesme_onaylari.json"
    
    # Test verisi oluştur
    test_verisi = [
        {
            "onay_id": "test_1",
            "kullanici_id": "user_123",
            "sozlesme_versiyonu": "V.2026-08-15",
            "durum": "onaylandi"
        },
        {
            "onay_id": "test_2",
            "kullanici_id": "user_456",
            "sozlesme_versiyonu": "V.2026-08-15",
            "durum": "onaylandi"
        }
    ]
    
    with open(test_dosyasi, "w", encoding="utf-8") as f:
        json.dump(test_verisi, f, ensure_ascii=False, indent=4)
    
    # Bridge oluştur
    bridge = AgentBridge()
    bridge.onay_dosyasi = test_dosyasi
    
    # onay_gecmisi çağır
    sonuc = bridge.onay_gecmisi()
    
    print(f"Sonuç: {json.dumps(sonuc, indent=2, ensure_ascii=False)}")
    
    # Beklenen sonuç kontrolü
    if sonuc["durum"] == "ebasarili" and sonuc["toplam_onay"] == 2:
        print("✅ Test BAŞARILI: Verili dosya için doğru sonuç döndürüldü")
    else:
        print("❌ Test BAŞARISIZ: Beklenen sonuç alınamadı")
    
    # Temizlik
    if os.path.exists(test_dosyasi):
        os.remove(test_dosyasi)
    
    print()

if __name__ == "__main__":
    print("agent_bridge.py onay_gecmisi Fonksiyonu Testleri")
    print("=" * 60)
    print()
    
    test_onay_gecmisi_bos_dosya()
    test_onay_gecmisi_bos_dosya_json()
    test_onay_gecmisi_verili_dosya()
    
    print("=" * 60)
    print("Tüm testler tamamlandı!")
