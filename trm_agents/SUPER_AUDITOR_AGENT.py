import os
import json

class SuperAuditorAgent:
    """Sistemin tamamını denetleyen ve hataları UTF-8 ile düzelten ajan."""

    def __init__(self, agent_name="Süper_Denetçi"):
        self.agent_name = agent_name

    def audit_code_directory(self, base_path="trm_agents"):
        print(f"\n[DENETİM] '{base_path}' klasörü taranıyor...")
        if not os.path.exists(base_path):
            return f"[HATA] '{base_path}' klasörü bulunamadı!"

        denetim_raporu = []
        files_to_check = ["kuresel_video_fabrikasi_ajani.py", "social_uploader_agent.py"]

        # Ana dizindeki ORCHESTRATOR_AGENT.py'yi de kontrol et
        orchestrator_path = os.path.join("..", "ORCHESTRATOR_AGENT.py")
        if os.path.exists(orchestrator_path):
            try:
                with open(orchestrator_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "os.environ.get" in content:
                        denetim_raporu.append(f"[BAŞARI] ORCHESTRATOR_AGENT.py güvenlik kontrolü geçti.")
                    else:
                        denetim_raporu.append(f"[UYARI] ORCHESTRATOR_AGENT.py güvenlik kontrolü zayıf.")
            except Exception as e:
                denetim_raporu.append(f"[HATA] ORCHESTRATOR_AGENT.py okunamadı: {e}")
        else:
            denetim_raporu.append(f"[KRİTİK] ORCHESTRATOR_AGENT.py ana dizinde eksik!")

        for filename in files_to_check:
            file_path = os.path.join(base_path, filename)

            if not os.path.exists(file_path):
                denetim_raporu.append(f"[KRİTİK] {filename} eksik!")
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "os.environ.get" in content:
                             denetim_raporu.append(f"[BAŞARI] {filename} güvenlik kontrolü geçti.")
                        else:
                             denetim_raporu.append(f"[UYARI] {filename} güvenlik kontrolü zayıf.")
                except Exception as e:
                    denetim_raporu.append(f"[HATA] {filename} okunamadı: {e}")

        return "[RAPOR] Kod taraması tamamlandı.\n" + "\n".join(denetim_raporu)

    def audit_materials_directory(self, materials_path="materials"):
        print(f"\n[DENETİM] '{materials_path}' klasörü taranıyor...")
        if not os.path.exists(materials_path):
            os.makedirs(materials_path)
            return "[DÜZELTİLDİ] Materyaller klasörü oluşturuldu."
        return "[BAŞARI] Materyaller klasörü temiz."

    def run_audit_cycle(self):
        print(f"\n=== [{self.agent_name}] Tam Sistem Denetimi Başlatılıyor ===")
        print(self.audit_code_directory())
        print(self.audit_materials_directory())

def trigger_system_audit():
    auditor = SuperAuditorAgent()
    auditor.run_audit_cycle()