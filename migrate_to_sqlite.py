#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: JSON to SQLite
Sosyal İmece Sistemi verilerini JSON'dan SQLite'a taşır
"""

from database_manager import DatabaseManager
from pathlib import Path
import json

def migrate_agents():
    """Migrate agents from JSON to SQLite"""
    db = DatabaseManager()
    
    # JSON dosya yolu
    json_path = Path(__file__).parent / "data" / "agents.json"
    
    print(f"[Migration] Starting migration from {json_path}")
    
    if db.migrate_agents_from_json(json_path):
        print("[Migration] Migration completed successfully")
        
        # Verify migration
        total_agents = db.get_total_agents_count()
        active_agents = db.get_active_agents_count()
        
        print(f"[Migration] Total agents in database: {total_agents}")
        print(f"[Migration] Active agents in database: {active_agents}")
        
        # Show sample data
        agents = db.get_all_agents()
        if agents:
            print(f"[Migration] Sample agent data (first 3):")
            for agent in agents[:3]:
                print(f"  - ID: {agent['id']}, Name: {agent['name']}, Status: {agent['status']}")
        
        return True
    else:
        print("[Migration] Migration failed")
        return False

if __name__ == "__main__":
    migrate_agents()
