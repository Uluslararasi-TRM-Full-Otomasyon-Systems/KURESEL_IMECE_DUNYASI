#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Orchestrator - Ana Orkestrator
Tum ajanlari yonetir ve koordine eder
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from web_scraper import TRMWebScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TRMOrchestrator:
    """TRM Ana Orkestrator"""
    
    def __init__(self):
        self.running = False
        self.agents = {}
        self.scraper = None
        self.start_time = None
    
    def initialize(self):
        """Sistemi baslat"""
        try:
            logger.info("TRM Orchestrator baslatiliyor...")
            
            # Web scraper yukle
            self.scraper = TRMWebScraper()
            
            # Baslama zamani
            self.start_time = datetime.now()
            
            logger.info("TRM Orchestrator baslatildi")
            return True
        except Exception as e:
            logger.error(f"Orchestrator baslatma hatasi: {e}")
            return False
    
    def add_agent(self, agent_name, agent_instance):
        """Ajan ekle"""
        self.agents[agent_name] = agent_instance
        logger.info(f"Ajan eklendi: {agent_name}")
    
    def remove_agent(self, agent_name):
        """Ajan kaldir"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Ajan kaldirildi: {agent_name}")
    
    def get_agent(self, agent_name):
        """Ajan al"""
        return self.agents.get(agent_name)
    
    def list_agents(self):
        """Tum ajanlari listele"""
        return list(self.agents.keys())
    
    async def run(self):
        """Ana dongu"""
        try:
            self.running = True
            logger.info("TRM Orchestrator calismaya basladi")
            
            while self.running:
                # Tum ajanlari calistir
                for agent_name, agent in self.agents.items():
                    if hasattr(agent, 'run'):
                        try:
                            await agent.run()
                        except Exception as e:
                            logger.error(f"Ajan hatasi ({agent_name}): {e}")
                
                # Bekle
                await asyncio.sleep(60)
                
        except Exception as e:
            logger.error(f"Ana dongu hatasi: {e}")
            self.running = False
    
    def stop(self):
        """Durdur"""
        self.running = False
        logger.info("TRM Orchestrator durduruldu")
    
    def get_status(self):
        """Durum raporu"""
        return {
            'running': self.running,
            'agents_count': len(self.agents),
            'agents': self.list_agents(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'scraper_loaded': self.scraper is not None
        }

if __name__ == "__main__":
    orchestrator = TRMOrchestrator()
    
    try:
        if orchestrator.initialize():
            print("TRM Orchestrator baslatildi")
            print("Durum:", orchestrator.get_status())
        else:
            print("Orchestrator baslatilamadi")
    except Exception as e:
        print(f"Hata: {e}")
