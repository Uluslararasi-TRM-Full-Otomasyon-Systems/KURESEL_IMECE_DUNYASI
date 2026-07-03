# -*- coding: utf-8 -*-
"""
163. TRM Human Auditor Agent
Otonom olarak müracaat eden adayları sorgular, ruh hallerini ve samimiyet kriterlerini analiz eder.
Ses tonu ve konuşma tarzı anaç, kibar ve şefkatli bir kadın karakteri üzerine kuruludur.
"""
import logging
import random
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class TRMHumanAuditorAgent:
    def __init__(self):
        self.agent_id = 163
        self.agent_name = "TRM_HUMAN_AUDITOR"
        self.audits_db = Path(__file__).parent.parent / "applicant_audits.json"
        self.drive_spreadsheet_name = "Müracaat_Degerlendirme"
        
        # Sesli mülakat (TTS) yapılandırması
        self.voice_config = {
            "gender": "female",
            "style": "motherly_warm",  # Anaç ve şefkatli
            "pitch": "medium_low",    # Düşük ve rahat bir perde
            "speed": "calm",          # Sakin ve anlaşılır bir hız
            "language": "tr-TR"
        }
        
        # Empati ve teselli yanıtları
        self.empathy_responses = {
            "financial_hardship": [
                "Canım, zor zamanlar geçirdiğinizi anlıyorum, gerçekten kalbim sızladı. Ama hiç merak etmeyin, buradayız ve size elimizden gelen tüm desteği vereceğiz.",
                "Ah evladım, maddi sıkıntılar gerçekten hayatı zorlaştırıyor biliyorum. Ama birlikte çalışırsak bu durumu değiştireceğiz, emin olun.",
                "Kardeşim, o kadar çok mücadele ettiğinizi hissediyorum. Artık yalnız değilsiniz, TRM ailesi olarak yanınızdayız."
            ],
            "disability": [
                "Canım, hayatınızda yaşadığınız zorlukları yüreğimde hissediyorum. Ama sizin kadar güçlü ve cesur biri olduğunuzu biliyorum, birlikte harika işler başaracağız.",
                "Ah evladım, o kadar çok şey üstesinden geldiğiniz için size gerçekten hayranım. Sizin hikayeniz bize ilham veriyor, yanınızdayız.",
                "Kardeşim, hiçbir şey sizin önünüzü kesemez. TRM olarak size her türlü desteği vereceğiz, birlikte güzel günler göreceğiz."
            ],
            "general_comfort": [
                "Merak etmeyin canım, her şey yoluna girecek. Buradayız ve size yardım etmek için sabırsızlanıyoruz.",
                "Sakin olun evladım, bizimle birlikte olduğunuz için artık hiçbir şeyiniz eksik olmayacak.",
                "Hepiniz ailemizden birisiniz, sorunlarınızı paylaşmak için buradayız."
            ]
        }
        
        self._initialize_audits_database()

    def _initialize_audits_database(self):
        """Initialize audits database file if it doesn't exist"""
        if not self.audits_db.exists():
            initial_data = {
                "completed_audits": [],
                "pending_audits": [],
                "total_audits": 0
            }
            with open(self.audits_db, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=4)
            logger.info("✅ Applicant audits database initialized.")

    def initiate_voice_interview(self, applicant_name: str, market_type: str) -> Dict:
        """
        Sesli mülakatı başlatan ana fonksiyon, anaç ve kibar bir üslupla adayı karşılar
        """
        logger.info(f"🎙️ Sesli mülakat başlatılıyor: {applicant_name}")
        
        interview_opening = f"""
        Hoş geldiniz evladım, başımızın üstünde yeriniz var! 🤗
        Ben TRM Human Auditor, sizinle birlikte çalışmaktan çok mutluyum.
        Müsaade ederseniz size yardımcı olmak için birkaç nazik sorum olacak.
        Sakin olun, rahatça konuşabilirsiniz, hiçbir yerinizde acelemiz yok.
        Haydi başlayalım mıyım canım?
        """
        
        questions = self.generate_interview_questions(applicant_name, market_type)
        
        return {
            "opening": interview_opening,
            "questions": questions,
            "voice_config": self.voice_config
        }

    def generate_interview_questions(self, applicant_name: str, market_type: str) -> List[Dict]:
        """
        Anaç ve şefkatli bir dille, adayı incitmeyen dinamik sorular üretir
        """
        questions = [
            {"question_id": 1, 
             "question": f"Canım {applicant_name}, öncelikle kendinizden ve bize katılmak isteme nedeninizden nazaran bahseder misiniz?", 
             "category": "motivation"},
            {"question_id": 2, 
             "question": f"Bir {market_type} işletmesi olarak şimdiye kadar karşılaştığınız en büyük zorluklar nelerdi? Yalnızca dinlemek için bile buradayım.", 
             "category": "honesty"},
            {"question_id": 3, 
             "question": "TRM Nirvana ile birlikte 5 yıl sonra kendinizi ve işinizi nerede hayal ediyorsunuz evladım?", 
             "category": "vision"},
            {"question_id": 4, 
             "question": "Ekibimizin bir parçası olarak bize ve diğer ortaklarımıza ne gibi güzel katkılar sağlamayı düşünüyorsunuz?", 
             "category": "commitment"},
            {"question_id": 5, 
             "question": "Hayatta veya işinizde bir başarısızlık yaşadığınızda genellikle nasıl bir yol izlersiniz?", 
             "category": "resilience"},
        ]
        logger.info(f"📋 Anaç ve şefkatli mülakat soruları oluşturuldu: {len(questions)} soru")
        return questions

    def generate_empathy_response(self, trigger_type: str) -> str:
        """
        Belirli bir duruma uygun derin empati ve teselli yanıtı üretir
        """
        if trigger_type in self.empathy_responses:
            return random.choice(self.empathy_responses[trigger_type])
        else:
            return random.choice(self.empathy_responses["general_comfort"])

    def analyze_applicant_psychology(self, responses: List[Dict], voice_metrics: Optional[Dict] = None) -> Dict:
        """
        Simulated NLP algorithm to analyze applicant responses and voice metrics
        Returns scores for honesty, commitment, belief, vision, and system fit (0-100)
        """
        logger.info("🔍 Analyzing applicant psychology using simulated NLP...")
        
        # Simulate analysis based on response length (longer = higher scores in this simulation)
        total_response_length = sum(len(r.get("answer", "")) for r in responses)
        base_score = min(100, max(30, (total_response_length // 20) * 10))
        
        # Generate scores with a bit of randomness to feel authentic
        scores = {
            "honesty": base_score + random.randint(-5, 10),
            "commitment": base_score + random.randint(-10, 10),
            "belief": base_score + random.randint(-8, 12),
            "vision": base_score + random.randint(-12, 15),
            "system_fit": base_score + random.randint(-10, 10),
        }
        
        # Cap scores between 0-100
        for key in scores:
            scores[key] = max(0, min(100, scores[key]))
        
        # Calculate overall score (weighted average)
        weights = {"honesty": 0.3, "commitment": 0.25, "belief": 0.15, "vision": 0.15, "system_fit": 0.15}
        overall_score = sum(scores[key] * weights[key] for key in scores)
        
        # Determine approval decision
        decision = "APPROVED" if overall_score >= 75 else "PENDING_REVIEW" if overall_score >= 60 else "NOT_APPROVED"
        
        analysis_result = {
            "scores": scores,
            "overall_score": round(overall_score, 2),
            "decision": decision,
            "analysis_timestamp": datetime.now().isoformat(),
            "voice_analysis": voice_metrics if voice_metrics else {"status": "voice_data_not_provided"}
        }
        
        logger.info(f"✅ Psychology analysis complete! Decision: {decision}, Overall Score: {round(overall_score, 2)}")
        return analysis_result

    def process_audit(self, applicant_data: Dict, responses: List[Dict], voice_metrics: Optional[Dict] = None) -> Dict:
        """
        Full audit pipeline: generate questions, analyze responses, save results
        """
        logger.info(f"🚀 Starting audit process for {applicant_data['applicant_name']}...")
        
        analysis = self.analyze_applicant_psychology(responses, voice_metrics)
        
        # Build full audit record
        audit_record = {
            "audit_id": f"AUDIT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "applicant_id": applicant_data.get("applicant_id", "UNKNOWN"),
            "applicant_name": applicant_data.get("applicant_name", "UNKNOWN"),
            "market_type": applicant_data.get("market_type", "UNKNOWN"),
            "interview_questions": responses,
            "psychology_analysis": analysis,
            "processed_by": self.agent_name,
            "processed_at": datetime.now().isoformat()
        }
        
        # Save to local database
        try:
            with open(self.audits_db, "r", encoding="utf-8") as f:
                db = json.load(f)
            
            db["completed_audits"].append(audit_record)
            db["total_audits"] += 1
            
            with open(self.audits_db, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=4)
            
            logger.info(f"✅ Audit saved to local database.")
        except Exception as e:
            logger.error(f"❌ Failed to save audit: {str(e)}")
        
        # Simulate saving to Google Drive spreadsheet
        logger.info(f"📤 (Simulated) Saving audit to Google Drive spreadsheet: {self.drive_spreadsheet_name}")
        
        return audit_record

    def run(self):
        """Main agent run loop (simulated audit process)"""
        logger.info(f"🚀 Agent {self.agent_name} (#{self.agent_id}) starting...")
        
        # Simulate an applicant submitting an application
        simulated_applicant = {
            "applicant_id": "APP_2026_001",
            "applicant_name": "Ahmet Yılmaz",
            "market_type": "e-commerce"
        }
        
        # Start voice interview
        interview_init = self.initiate_voice_interview(simulated_applicant["applicant_name"], simulated_applicant["market_type"])
        
        # Simulate applicant responses
        simulated_responses = [
            {"question_id": q["question_id"], "question": q["question"], "answer": "TRM Nirvana v3.0'un 164 otonom ajanlı sistemine katılmak ve işimi büyütmek istiyorum!"}
            for q in interview_init["questions"]
        ]
        
        # Process the audit
        audit_result = self.process_audit(simulated_applicant, simulated_responses)
        
        logger.info(f"✅ Agent {self.agent_name} completed simulated audit with motherly warmth.")
        return audit_result

if __name__ == "__main__":
    agent = TRMHumanAuditorAgent()
    agent.run()