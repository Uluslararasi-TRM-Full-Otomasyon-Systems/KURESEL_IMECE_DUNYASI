import os
import time
import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass(frozen=True)
class AgentGorevi:
    ad: str
    birincil: object
    yedek: object | None = None
    azami_deneme: int = 2


class Orchestrator:
    def __init__(self, azami_isci=8, log_yolu="logs/orchestrator.log"):
        self.azami_isci = int(azami_isci) if int(azami_isci) > 0 else 1
        self.logger = logging.getLogger("trm_orchestrator")
        if not self.logger.handlers:
            os.makedirs(os.path.dirname(log_yolu) or ".", exist_ok=True)
            handler = RotatingFileHandler(
                log_yolu,
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8",
            )
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _calistir(self, gorev: AgentGorevi):
        if not callable(gorev.birincil):
            raise TypeError(f"Birincil ajan cagirilan degil: {gorev.ad}")

        son_hata = None
        for deneme in range(1, max(1, gorev.azami_deneme) + 1):
            try:
                baslangic = time.time()
                sonuc = gorev.birincil()
                sure = round(time.time() - baslangic, 3)
                self.logger.info("OK ad=%s deneme=%s sure_s=%s", gorev.ad, deneme, sure)
                return {"ad": gorev.ad, "durum": "ok", "sonuc": sonuc, "deneme": deneme, "sure_s": sure}
            except Exception as e:
                son_hata = e
                self.logger.exception("ERR ad=%s deneme=%s", gorev.ad, deneme)

        if gorev.yedek is not None:
            try:
                baslangic = time.time()
                sonuc = gorev.yedek() if callable(gorev.yedek) else None
                sure = round(time.time() - baslangic, 3)
                if sonuc is not None:
                    self.logger.info("OK_YEDEK ad=%s sure_s=%s", gorev.ad, sure)
                    return {"ad": gorev.ad, "durum": "ok_yedek", "sonuc": sonuc, "deneme": gorev.azami_deneme, "sure_s": sure}
            except Exception:
                self.logger.exception("ERR_YEDEK ad=%s", gorev.ad)

        return {"ad": gorev.ad, "durum": "hata", "sonuc": None, "hata": str(son_hata) if son_hata else "Bilinmeyen hata"}

    def swarm_calistir(self, gorevler):
        gorev_listesi = list(gorevler or [])
        if not gorev_listesi:
            return []

        sonuclar = []
        with ThreadPoolExecutor(max_workers=self.azami_isci) as havuz:
            gelecekler = {havuz.submit(self._calistir, g): g for g in gorev_listesi}
            for gelecek in as_completed(gelecekler):
                try:
                    sonuclar.append(gelecek.result())
                except Exception as e:
                    g = gelecekler[gelecek]
                    self.logger.exception("FATAL ad=%s", getattr(g, "ad", "Bilinmiyor"))
                    sonuclar.append({"ad": getattr(g, "ad", "Bilinmiyor"), "durum": "hata", "sonuc": None, "hata": str(e)})

        return sonuclar
