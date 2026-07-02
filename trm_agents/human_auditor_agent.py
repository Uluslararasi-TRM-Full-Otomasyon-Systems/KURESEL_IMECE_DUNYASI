# -*- coding: utf-8 -*-
"""
163. TRM Human Auditor Agent
Otonom olarak müracaat eden adayları sorgular, ruh hallerini ve samimiyet kriterlerini analiz eder.
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
        self.drive_spreadsheet_name = "Müracaat_Degerlendirme"  # Simulated for now
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

    def generate_interview_questions(self, applicant_name: str, market_type: str) -> List[Dict]:
        """
        Generate dynamic, empathetic interview questions for the applicant
        """
        questions = [
            {"question_id": 1, "question": f"Merhaba {applicant_name}! Öncelikle kendinizden ve neden TRM Nirvana v3.0'a katılmak istediğinizden bahseder misiniz?", "category": "motivation"},
            {"question_id": 2, "question": f"Bir {market_type} işletmesi olarak en büyük zorluklarınız nelerdi?", "category": "honesty"},
            {"question_id": 3, "question": "TRM Nirvana ile birlikte 5 yıl sonra nerede olmayı hayal ediyorsunuz?", "category": "vision"},
            {"question_id": 4, "question": "Ekibimizin bir parçası olarak bize ne gibi katkılar sağlamayı planlıyorsunuz?", "category": "commitment"},
            {"question_id": 5, "question": "Üretimde veya pazarlamada bir başarısızlık yaşadığınızda nasıl tepki verirdiniz?", "category": "resilience"},
        ]
        logger.info(f"📋 Generated {len(questions)} interview questions for {applicant_name}.")
        return questions

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
        
        questions = self.generate_interview_questions(simulated_applicant["applicant_name"], simulated_applicant["market_type"])
        
        # Simulate applicant responses
        simulated_responses = [
            {"question_id": q["question_id"], "question": q["question"], "answer": "TRM Nirvana v3.0'un 162 otonom ajanlı sistemine katılmak ve işimi büyütmek istiyorum!"}
            for q in questions
        ]
        
        # Process the audit
        audit_result = self.process_audit(simulated_applicant, simulated_responses)
        
        logger.info(f"✅ Agent {self.agent_name} completed simulated audit.")
        return audit_result

if __name__ == "__main__":
    agent = TRMHumanAuditorAgent()
    agent.run()