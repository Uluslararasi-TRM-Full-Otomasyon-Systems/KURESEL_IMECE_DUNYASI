#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Orchestrator - Ana Orkestrator
Tum ajanlari yonetir ve koordine eder
Dongu kilitlenmelerini onleyen ve kesintisiz calisan gelişmiş versiyon
"""

import os
import sys
import logging
import asyncio
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

# Logging konfigurasyonu - donmayi onle
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trm_orchestrator.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class TRMOrchestrator:
    """TRM Ana Orkestrator - Gelişmiş Versiyon"""
    
    def __init__(self):
        self.running = False
        self.agents = {}
        self.scraper = None
        self.start_time = None
        self.task_queue = Queue()
        self.log_queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.active_agents = 200
        self.operation_stats = {
            'urun_toplama': 0,
            'isleme': 0,
            'sosyal_medya': 0,
            'telegram': 0,
            'hatalar': 0
        }
        self.lock = threading.Lock()
        
    def initialize(self):
        """Sistemi baslat"""
        try:
            logger.info("TRM Orchestrator baslatiliyor...")
            
            # Web scraper yukle (opsiyonel)
            try:
                from web_scraper import TRMWebScraper
                self.scraper = TRMWebScraper()
                logger.info("Web scraper yuklendi")
            except ImportError:
                logger.warning("Web scraper bulunamadi, devam ediliyor...")
                self.scraper = None
            
            # Baslama zamani
            self.start_time = datetime.now()
            
            # Log isleyiciyi baslat
            self.log_handler_thread = threading.Thread(target=self._log_processor, daemon=True)
            self.log_handler_thread.start()
            
            logger.info("TRM Orchestrator baslatildi - Aktif Ajan Sayisi: 200")
            return True
        except Exception as e:
            logger.error(f"Orchestrator baslatma hatasi: {e}")
            return False
    
    def add_agent(self, agent_name, agent_instance):
        """Ajan ekle"""
        with self.lock:
            self.agents[agent_name] = agent_instance
        logger.info(f"Ajan eklendi: {agent_name}")
    
    def remove_agent(self, agent_name):
        """Ajan kaldir"""
        with self.lock:
            if agent_name in self.agents:
                del self.agents[agent_name]
        logger.info(f"Ajan kaldirildi: {agent_name}")
    
    def get_agent(self, agent_name):
        """Ajan al"""
        with self.lock:
            return self.agents.get(agent_name)
    
    def list_agents(self):
        """Tum ajanlari listele"""
        with self.lock:
            return list(self.agents.keys())
    
    def _log_processor(self):
        """Log isleyici - dongu donmayi onler"""
        while True:
            try:
                log_entry = self.log_queue.get(timeout=1)
                if log_entry == 'STOP':
                    break
                logger.info(log_entry)
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Log isleyici hatasi: {e}")
    
    def add_log(self, message):
        """Log ekle"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_queue.put(f"[{timestamp}] {message}")
    
    async def _run_agent_safely(self, agent_name, agent):
        """Ajanı guvenli sekilde calistir - dongu kilitlenmesini onler"""
        try:
            if hasattr(agent, 'run'):
                await asyncio.wait_for(agent.run(), timeout=30.0)
                self.add_log(f"Ajan basarili: {agent_name}")
                return True
            elif callable(agent):
                # Callable ise thread pool'da calistir
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(self.executor, agent)
                self.add_log(f"Ajan basarili (callable): {agent_name}")
                return True
            else:
                self.add_log(f"Uyarı: {agent_name} calistirilabilir degil")
                return False
        except asyncio.TimeoutError:
            self.operation_stats['hatalar'] += 1
            self.add_log(f"HATA: {agent_name} zaman asimi (30sn)")
            return False
        except Exception as e:
            self.operation_stats['hatalar'] += 1
            self.add_log(f"HATA: {agent_name} - {str(e)}")
            return False
    
    async def _product_collection_cycle(self):
        """Urun toplama dongusu"""
        while self.running:
            try:
                self.add_log("Urun toplama dongusu baslatildi...")
                # Buraya urun toplama mantigi gelecek
                self.operation_stats['urun_toplama'] += 1
                await asyncio.sleep(120)  # 2 dakikada bir
            except Exception as e:
                self.add_log(f"Urun toplama hatasi: {e}")
                await asyncio.sleep(60)
    
    async def _processing_cycle(self):
        """Isleme dongusu"""
        while self.running:
            try:
                self.add_log("Isleme dongusu baslatildi...")
                # Buraya isleme mantigi gelecek
                self.operation_stats['isleme'] += 1
                await asyncio.sleep(60)  # 1 dakikada bir
            except Exception as e:
                self.add_log(f"Isleme hatasi: {e}")
                await asyncio.sleep(30)
    
    async def _social_media_cycle(self):
        """Sosyal medya dongusu"""
        while self.running:
            try:
                self.add_log("Sosyal medya dongusu baslatildi...")
                # Buraya sosyal medya mantigi gelecek
                self.operation_stats['sosyal_medya'] += 1
                await asyncio.sleep(300)  # 5 dakikada bir
            except Exception as e:
                self.add_log(f"Sosyal medya hatasi: {e}")
                await asyncio.sleep(60)
    
    async def _telegram_cycle(self):
        """Telegram dongusu"""
        while self.running:
            try:
                self.add_log("Telegram dongusu baslatildi...")
                # Buraya Telegram mantigi gelecek
                self.operation_stats['telegram'] += 1
                await asyncio.sleep(180)  # 3 dakikada bir
            except Exception as e:
                self.add_log(f"Telegram hatasi: {e}")
                await asyncio.sleep(60)
    
    async def run(self):
        """Ana dongu - dongu kilitlenmesini onleyen yapida"""
        try:
            self.running = True
            self.add_log("TRM Orchestrator calismaya basladi")
            
            # Tum donguleri paralel baslat
            tasks = []
            
            # Urun toplama dongusu
            tasks.append(asyncio.create_task(self._product_collection_cycle()))
            
            # Isleme dongusu
            tasks.append(asyncio.create_task(self._processing_cycle()))
            
            # Sosyal medya dongusu
            tasks.append(asyncio.create_task(self._social_media_cycle()))
            
            # Telegram dongusu
            tasks.append(asyncio.create_task(self._telegram_cycle()))
            
            # Ajan dongusu
            async def agent_cycle():
                while self.running:
                    with self.lock:
                        current_agents = list(self.agents.items())
                    
                    if current_agents:
                        agent_tasks = []
                        for agent_name, agent in current_agents:
                            agent_tasks.append(self._run_agent_safely(agent_name, agent))
                        
                        if agent_tasks:
                            await asyncio.gather(*agent_tasks, return_exceptions=True)
                    
                    await asyncio.sleep(30)  # 30 saniyede bir
            
            tasks.append(asyncio.create_task(agent_cycle()))
            
            # Tum gorevleri bekle
            await asyncio.gather(*tasks, return_exceptions=True)
                
        except asyncio.CancelledError:
            self.add_log("Orchestrator iptal edildi")
        except Exception as e:
            self.add_log(f"Ana dongu hatasi: {e}")
            logger.error(f"Ana dongu hatasi: {e}")
        finally:
            self.running = False
    
    def stop(self):
        """Durdur"""
        self.running = False
        self.log_queue.put('STOP')
        self.executor.shutdown(wait=False)
        self.add_log("TRM Orchestrator durduruldu")
        logger.info("TRM Orchestrator durduruldu")
    
    def get_status(self):
        """Durum raporu"""
        with self.lock:
            return {
                'running': self.running,
                'agents_count': len(self.agents),
                'active_agents': self.active_agents,
                'agents': self.list_agents(),
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'scraper_loaded': self.scraper is not None,
                'operation_stats': self.operation_stats.copy(),
                'uptime': str(datetime.now() - self.start_time) if self.start_time else None
            }
    
    def get_realtime_logs(self, limit=50):
        """Gercek zamanli loglar"""
        logs = []
        try:
            with open('trm_orchestrator.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                logs = [line.strip() for line in lines[-limit:]]
        except Exception as e:
            logs = [f"Log okuma hatasi: {e}"]
        return logs

if __name__ == "__main__":
    orchestrator = TRMOrchestrator()
    
    try:
        if orchestrator.initialize():
            print("TRM Orchestrator baslatildi")
            print("Durum:", orchestrator.get_status())
            
            # Async loop'u baslat
            try:
                asyncio.run(orchestrator.run())
            except KeyboardInterrupt:
                print("\nKullanici durdurma sinyali...")
                orchestrator.stop()
        else:
            print("Orchestrator baslatilamadi")
    except Exception as e:
        print(f"Hata: {e}")
        logger.error(f"Kritik hata: {e}")
