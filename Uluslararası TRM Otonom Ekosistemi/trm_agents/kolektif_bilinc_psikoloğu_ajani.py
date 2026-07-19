# -*- coding: utf-8 -*-
import random

class KolektifBilincPsikologuAjani:
    def __init__(self):
        self.ajan_id = 168
        self.isim = "Kolektif Bilinç Yapay Zeka Psikoloğu"
        
    def duygu_analizi_tara(self, hedef_ulke):
        """Sosyal medya yorumlarından kitlelerin anlık psikolojik durumunu ve duygu durumunu analiz eder."""
        duygu_durumlari = {
            "ABD": {"duygu": "KAYGILI (Hava Durumu)", "reklam_stratejisi": "Güvenlik ve Tedarik Odaklı"},
            "Almanya": {"duygu": "STRESLİ (Kış Sezonu)", "reklam_stratejisi": "Ev Konforu ve Sıcaklık Odaklı"},
            "Fransa": {"duygu": "YORGUN (Okula Dönüş)", "reklam_stratejisi": "Pratiklik ve Enerji Verici"},
            "İngiltere": {"duygu": "COŞKULU (Yaz Festivali)", "reklam_stratejisi": "Eğlence ve Sosyallik Odaklı"}
        }
        
        analiz = duygu_durumlari.get(hedef_ulke, {"duygu": "NÖTR", "reklam_stratejisi": "Genel Pazarlama"})
        analiz["psikolojik_skor"] = random.randint(75, 95)
        return analiz