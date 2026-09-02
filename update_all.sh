#!/bin/bash

echo "========================================="
echo "   SİSTEM GÜNCELLEME (165 → 200)"
echo "========================================="

# 1. Yedek al
echo "📁 Yedek alınıyor..."
mkdir -p yedek_$(date +%Y%m%d_%H%M%S)
cp -r ./* yedek_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null

# 2. Derya → Mehmet değiştir
echo "🔄 Derya → Mehmet değiştiriliyor..."
find . -type f \( -name "*.py" -o -name "*.html" -o -name "*.js" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.txt" -o -name "*.md" -o -name "*.sh" \) -exec sed -i 's/Derya/Mehmet/g' {} \;

# 3. 165 → 200 değiştir
echo "🔄 165 → 200 değiştiriliyor..."
find . -type f \( -name "*.py" -o -name "*.html" -o -name "*.js" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" \) -exec sed -i 's/165/200/g' {} \;

# 4. config.json güncelle (yoksa oluştur)
echo "📝 config.json güncelleniyor..."
cat > config.json << 'EOF'
{
    "max_agents": 200,
    "orchestrator": {"host": "0.0.0.0", "port": 8080},
    "agent_defaults": {"status": "active"}
}
EOF

# 5. state.yaml güncelle
echo "📝 state.yaml güncelleniyor..."
cat > state.yaml << 'EOF'
system:
  status: "running"
  version: "3.0.0"
agents:
  total: 200
  active: 0
EOF

# 6. logs klasörünü oluştur
mkdir -p logs data

echo "========================================="
echo "✅ GÜNCELLEME TAMAMLANDI!"
echo "📌 Orchestrator'ı başlatın: python3 orchestrator.py"
echo "📌 Panel sayfasını yenileyin (Ctrl+F5)"
echo "========================================="