# -*- coding: utf-8 -*-
import random

class DinamikLinkDonusturucuAjani:
    def __init__(self):
        self.ajan_id = 167
        self.isim = "Dinamik Link ve Komisyon Donusturucu"
        
    def kuresel_en_yuksek_komisyonu_bagla(self, arbitraj_verisi, trend_verisi):
        """Fiyat farki ve talebi birlestirip en yuksek komisyonlu affiliate linkini uretir."""
        optimize_linkler = []
        
        for t in trend_verisi:
            for a in arbitraj_verisi:
                if t["urun"] == a["urun"]:
                    normal_komisyon = 10
                    kuresel_komisyon = normal_komisyon + random.randint(10, 15) # %20-%25 arasi komisyon
                    
                    optimize_linkler.append({
                        "urun": t["urun"],
                        "hedef_ulke": t["ulke"],
                        "talep_nedeni": t["sebep"],
                        "tavsiye_edilen_komisyon": f"%{kuresel_komisyon}",
                        "pilot_grup_link": f"https://trm.market/affiliate/pilot_group/{t['urun']}?geo={t['ulke']}",
                        "durum": "LINK HAZIR / OTOMATIK"
                    })
        return optimize_linkler