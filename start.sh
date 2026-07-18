#!/bin/bash

echo "========================================="
echo "   SOSYAL İMECE DÜNYA - BAŞLATILIYOR"
echo "========================================="

# 1. Orchestrator'ı başlat
echo "🚀 Orchestrator başlatılıyor..."
python3 orchestrator.py &
ORCHESTRATOR_PID=$!
echo "✅ Orchestrator PID: $ORCHESTRATOR_PID"

# 2. Ajanları başlat (200 ajan)
echo "🤖 Ajanlar başlatılıyor..."
for i in {1..200}; do
    if [ $i -eq 200 ]; then
        echo "   🟣 DNP Ajan (Agent-200) başlatılıyor..."
        python3 agent_200.py &
    else
        # Diğer ajanlar
        echo "   ⚪ Agent-$i başlatılıyor..."
        python3 agent.py --id $i &
    fi
done

echo "========================================="
echo "✅ TÜM SİSTEM BAŞLATILDI"
echo "📊 Orchestrator: http://localhost:8080"
echo "📱 Panel: panel.html dosyasını açın"
echo "========================================="

# Bekle
wait