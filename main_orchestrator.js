/**
 * main_orchestrator.js
 * TRM NIRVANA v3.0 - 200 Ajanlı Otomasyon Sistemi Entegrasyon Katmanı
 * Modüler yapı, merkezi state yönetimi, metrik takibi ve ajanlar arası iletişim
 * 
 * @version 3.1.0
 * @author Mehmet - TRM NIRVANA Ekibi
 */

const Orchestrator = {
    // ----- SİSTEM STATE -----
    state: {
        agents: [],
        systemStatus: 'idle',
        cpuLoad: 0,
        activeAgents: 0,
        lastUpdate: null,
        isRunning: false,
        metrics: {
            satisBasarisi: 98.0,
            ajanHataOrani: 0.2,
            toplamIslem: 0,
            basariliIslem: 0,
            hataliIslem: 0
        },
        safetyMode: false
    },

    // ----- AJAN LİSTESİ -----
    agentTypes: {
        CONTENT: 'content',
        SEO: 'seo',
        FINANCE: 'finance',
        SALES: 'sales',
        DNP: 'dnp'
    },

    // ----- BAŞLANGIÇ -----
    init: function() {
        console.log("🚀 TRM Orchestrator v3.1 başlatılıyor...");
        
        // 200 ajanı oluştur
        this.createAgents(200);
        
        // Event listener'ları kur
        this.setupEventListeners();
        
        // Sistem durumunu güncelle
        this.updateSystemStatus('ready');
        
        // Metrikleri güncelle
        this.updateMetrics();
        
        console.log(`✅ Orchestrator hazır! ${this.state.agents.length} ajan aktif.`);
        return this;
    },

    // ----- AJAN OLUŞTURMA -----
    createAgents: function(count) {
        const agents = [];
        const roles = ['content', 'seo', 'finance', 'sales', 'admin'];
        
        for (let i = 1; i <= count; i++) {
            const role = roles[i % roles.length];
            const isDNP = (i === count && count >= 161);
            
            agents.push({
                id: i,
                kod: `Agent-${i.toString().padStart(3, '0')}`,
                rol: isDNP ? 'dnp' : role,
                aktif: false,
                cpu: 0,
                apiGecikme: 0,
                gorev: this.getAgentTask(i, role, isDNP),
                webAdres: isDNP ? 'dnp.imece.ai' : `agent${i}.imece.ai`,
                sonGuncelleme: null,
                islemSayisi: 0,
                basariliIslem: 0,
                hataliIslem: 0,
                hataOrani: 0
            });
        }
        
        this.state.agents = agents;
        this.state.activeAgents = agents.length;
    },

    // ----- AJAN GÖREV ATAMA -----
    getAgentTask: function(id, role, isDNP) {
        if (isDNP) return "🤖 DNP Ajan | Sistem Bütünlüğü ve Optimizasyon";
        
        const tasks = {
            content: ['İçerik Üretimi', 'Blog Yazımı', 'Sosyal Medya Yönetimi', 'Makale Yazımı'],
            seo: ['SEO Optimizasyonu', 'Anahtar Kelime Analizi', 'Backlink Yönetimi'],
            finance: ['Finans Analizi', 'Affiliate Yönetimi', 'Bütçe Takibi'],
            sales: ['Satış Yönetimi', 'Müşteri İlişkileri', 'Pazarlama Otomasyonu'],
            admin: ['Sistem Yönetimi', 'Koordinasyon', 'Denetim']
        };
        
        const taskList = tasks[role] || tasks.admin;
        return taskList[id % taskList.length];
    },

    // ----- EVENT LISTENER'LAR -----
    setupEventListeners: function() {
        document.addEventListener('DOMContentLoaded', () => {
            console.log("📄 DOM yüklendi, Orchestrator aktif.");
            this.syncWithUI();
        });

        // CPU güncelleme
        window.addEventListener('cpuUpdate', (e) => {
            if (e.detail && typeof e.detail.cpu !== 'undefined') {
                this.updateCPU(e.detail.cpu);
            }
        });

        // Sistem durumu değişiklikleri
        document.addEventListener('systemStatusChange', (e) => {
            if (e.detail && e.detail.status) {
                this.updateSystemStatus(e.detail.status);
            }
        });

        // Self-Healing olaylarını dinle
        document.addEventListener('selfHealingEvent', (e) => {
            if (e.detail) {
                this.handleSelfHealingEvent(e.detail);
            }
        });
    },

    // ----- SELF-HEALING OLAY YÖNETİCİSİ -----
    handleSelfHealingEvent: function(detail) {
        if (detail.type === 'hata') {
            // Hata tespit edildi - hata oranını artır
            this.state.metrics.hataliIslem++;
            this.state.metrics.toplamIslem++;
            this.updateMetrics();
            
            // Hata oranı %2'yi aşarsa uyarı modu
            if (this.state.metrics.ajanHataOrani > 2.0) {
                this.triggerSafetyMode();
            }
        } else if (detail.type === 'cozum') {
            // Çözüm bulundu - başarı oranını artır
            this.state.metrics.basariliIslem++;
            this.state.metrics.toplamIslem++;
            this.updateMetrics();
        }
        
        // Harekat loguna ekle
        this.addHealingLog(detail);
    },

    // ----- METRİKLERİ GÜNCELLE -----
    updateMetrics: function() {
        const metrics = this.state.metrics;
        const total = metrics.toplamIslem || 1;
        
        // Satış Başarısı = (Başarılı İşlem / Toplam İşlem) * 100
        const satisBasarisi = (metrics.basariliIslem / total) * 100;
        metrics.satisBasarisi = Math.min(100, Math.max(0, satisBasarisi));
        
        // Ajan Hata Oranı = (Hatalı İşlem / Toplam İşlem) * 100
        const hataOrani = (metrics.hataliIslem / total) * 100;
        metrics.ajanHataOrani = Math.min(100, Math.max(0, hataOrani));
        
        // UI'ı güncelle
        this.updateMetricsDisplay();
        
        // Sistem sağlığını kontrol et
        if (metrics.ajanHataOrani > 2.0) {
            this.triggerSafetyMode();
        }
    },

    // ----- METRİK GÖSTERGESİNİ GÜNCELLE -----
    updateMetricsDisplay: function() {
        const satisEl = document.getElementById('satisBasarisi');
        const hataEl = document.getElementById('ajanHataOrani');
        const saglikEl = document.getElementById('sistemSaglikDetay');
        const indicatorEl = document.getElementById('saglikIndicator');
        
        if (satisEl) {
            const value = this.state.metrics.satisBasarisi;
            satisEl.textContent = `%${value.toFixed(1)}`;
            satisEl.style.color = value > 90 ? '#66ff66' : (value > 70 ? '#ffaa33' : '#ff6666');
        }
        
        if (hataEl) {
            const value = this.state.metrics.ajanHataOrani;
            hataEl.textContent = `%${value.toFixed(2)}`;
            hataEl.style.color = value < 1.0 ? '#66ff66' : (value < 2.0 ? '#ffaa33' : '#ff6666');
        }
        
        // Sistem sağlığını güncelle
        if (this.state.metrics.ajanHataOrani > 2.0) {
            if (saglikEl) {
                saglikEl.textContent = '⚠️ Uyarı - Yüksek Hata Oranı';
                saglikEl.style.color = '#ffaa33';
            }
            if (indicatorEl) {
                indicatorEl.className = 'health-indicator health-yellow';
            }
        } else {
            if (saglikEl) {
                saglikEl.textContent = '✅ Çalışıyor';
                saglikEl.style.color = '#4caf50';
            }
            if (indicatorEl) {
                indicatorEl.className = 'health-indicator health-green';
            }
        }
    },

    // ----- GÜVENLİ MOD TRİGGER -----
    triggerSafetyMode: function() {
        if (!this.state.safetyMode) {
            this.state.safetyMode = true;
            console.warn("⚠️ SAFETY MODE AKTİF! Hata oranı %2'yi aştı.");
            this.updateSystemStatus('paused');
            
            // Log'a ekle
            this.addLog("🚨 SAFETY MODE - Hata oranı %2'yi aştı. Sistem duraklatıldı.");
            
            // UI bildirimi
            const saglikEl = document.getElementById('sistemSaglikDetay');
            if (saglikEl) {
                saglikEl.textContent = '🔴 ACİL DURUM - YÜKSEK HATA';
                saglikEl.style.color = '#ff4444';
            }
            
            // Event fırlat
            document.dispatchEvent(new CustomEvent('safetyModeTriggered', {
                detail: { 
                    hataOrani: this.state.metrics.ajanHataOrani,
                    timestamp: new Date()
                }
            }));
        }
    },

    // ----- HAREKAT LOGUNA EKLE -----
    addHealingLog: function(detail) {
        const timeline = document.getElementById('healingTimeline');
        if (!timeline) return;
        
        // "Henüz" mesajını kaldır
        if (timeline.children.length === 1 && timeline.children[0].innerText.includes('Henüz')) {
            timeline.innerHTML = '';
        }
        
        const item = document.createElement('div');
        item.className = 'healing-item';
        const time = new Date().toLocaleTimeString();
        const badgeClass = detail.type === 'hata' ? 'hata' : (detail.type === 'cozum' ? 'cozum' : 'bilgi');
        const badgeText = detail.type === 'hata' ? '⚠️ Hata' : (detail.type === 'cozum' ? '✅ Çözüm' : 'ℹ️ Bilgi');
        
        item.innerHTML = `
            <span class="time">${time}</span>
            <span class="badge ${badgeClass}">${badgeText}</span>
            <span class="desc">${detail.mesaj || 'Sistem olayı kaydedildi.'}</span>
        `;
        
        timeline.prepend(item);
        while (timeline.children.length > 20) {
            timeline.removeChild(timeline.lastChild);
        }
    },

    // ----- CPU VERİSİ GÜNCELLEME -----
    updateCPU: function(cpuValue) {
        const normalizedCPU = Math.min(100, Math.max(0, cpuValue));
        this.state.cpuLoad = normalizedCPU;
        this.state.lastUpdate = new Date();
        
        this.updateCPUIDisplay(normalizedCPU);
        
        const event = new CustomEvent('cpuUpdated', {
            detail: { 
                cpu: normalizedCPU,
                timestamp: this.state.lastUpdate
            }
        });
        document.dispatchEvent(event);
        
        return this;
    },

    // ----- CPU GÖSTERGESİNİ GÜNCELLE -----
    updateCPUIDisplay: function(cpuValue) {
        const cpuStatusEl = document.getElementById('cpu-status');
        const cpuBarEl = document.getElementById('cpu-bar');
        const cpuTimeEl = document.getElementById('cpuSonGuncelleme');
        
        if (cpuStatusEl) {
            let color = '#4caf50';
            if (cpuValue > 80) color = '#f44336';
            else if (cpuValue > 60) color = '#ffaa33';
            
            cpuStatusEl.textContent = `${Math.round(cpuValue)}%`;
            cpuStatusEl.style.color = color;
        }
        
        if (cpuBarEl) {
            cpuBarEl.style.width = `${cpuValue}%`;
            if (cpuValue > 80) {
                cpuBarEl.style.background = 'linear-gradient(90deg, #f44336, #d32f2f)';
            } else if (cpuValue > 60) {
                cpuBarEl.style.background = 'linear-gradient(90deg, #ffaa33, #f57c00)';
            } else {
                cpuBarEl.style.background = 'linear-gradient(90deg, #4caf50, #2e7d32)';
            }
        }
        
        if (cpuTimeEl) {
            const now = new Date();
            cpuTimeEl.textContent = now.toLocaleTimeString('tr-TR');
        }
    },

    // ----- SİSTEM DURUMU -----
    updateSystemStatus: function(status) {
        const validStatus = ['idle', 'ready', 'running', 'paused', 'error'];
        if (validStatus.includes(status)) {
            this.state.systemStatus = status;
            this.state.isRunning = (status === 'running');
            
            const statusEl = document.querySelector('#system-status');
            if (statusEl) {
                statusEl.textContent = status.toUpperCase();
                statusEl.style.color = status === 'running' ? '#4caf50' : (status === 'paused' ? '#ffaa33' : '#ff6666');
            }
            
            console.log(`📊 Sistem durumu: ${status}`);
        }
    },

    // ----- AJAN KOMUT GÖNDER -----
    dispatchCommand: function(agentId, command, payload = null) {
        const agent = this.state.agents.find(a => a.id === agentId || a.kod === agentId);
        if (!agent) {
            console.warn(`⚠️ Ajan ${agentId} bulunamadı.`);
            return false;
        }
        
        console.log(`📨 Ajan ${agent.kod} için komut: ${command}`, payload || '');
        
        switch(command) {
            case 'start':
                agent.aktif = true;
                agent.sonGuncelleme = new Date();
                break;
            case 'stop':
                agent.aktif = false;
                break;
            case 'status':
                return { ...agent };
            case 'record_success':
                agent.basariliIslem++;
                agent.islemSayisi++;
                this.state.metrics.basariliIslem++;
                this.state.metrics.toplamIslem++;
                this.updateMetrics();
                break;
            case 'record_error':
                agent.hataliIslem++;
                agent.islemSayisi++;
                this.state.metrics.hataliIslem++;
                this.state.metrics.toplamIslem++;
                this.updateMetrics();
                break;
            default:
                const event = new CustomEvent('agentCommand', {
                    detail: { agent, command, payload }
                });
                document.dispatchEvent(event);
        }
        
        return true;
    },

    // ----- TOPLU AJAN KONTROL -----
    broadcastCommand: function(command, payload = null) {
        console.log(`📢 Tüm ajanlara komut: ${command}`);
        this.state.agents.forEach(agent => {
            this.dispatchCommand(agent.kod, command, payload);
        });
        return this;
    },

    // ----- SİSTEMİ BAŞLAT -----
    startSystem: function() {
        if (this.state.isRunning) {
            console.log("⚠️ Sistem zaten çalışıyor.");
            return this;
        }
        
        if (this.state.safetyMode) {
            console.warn("⚠️ Safety Mode aktif! Önce safety mode'u kapatmalısınız.");
            return this;
        }
        
        console.log("▶️ Sistem başlatılıyor...");
        this.broadcastCommand('start');
        this.updateSystemStatus('running');
        
        document.dispatchEvent(new CustomEvent('systemStarted'));
        
        return this;
    },

    // ----- SİSTEMİ DURDUR -----
    stopSystem: function() {
        if (!this.state.isRunning) {
            console.log("⚠️ Sistem zaten durdurulmuş.");
            return this;
        }
        
        console.log("⏹️ Sistem durduruluyor...");
        this.broadcastCommand('stop');
        this.updateSystemStatus('idle');
        
        document.dispatchEvent(new CustomEvent('systemStopped'));
        
        return this;
    },

    // ----- SAFETY MODE'U KAPAT -----
    disableSafetyMode: function() {
        if (this.state.safetyMode) {
            this.state.safetyMode = false;
            this.updateSystemStatus('idle');
            this.addLog("🟢 Safety Mode devre dışı bırakıldı. Sistem normal çalışmaya hazır.");
            
            document.dispatchEvent(new CustomEvent('safetyModeDisabled'));
        }
        return this;
    },

    // ----- UI İLE SENKRONİZASYON -----
    syncWithUI: function() {
        const agentGrid = document.getElementById('agentGrid');
        if (agentGrid) {
            console.log("🔄 Ajan grid'i senkronize ediliyor...");
        }
        
        this.updateCPUIDisplay(this.state.cpuLoad || 0);
        this.updateMetricsDisplay();
        
        const statusEl = document.querySelector('#system-status');
        if (statusEl) {
            statusEl.textContent = this.state.systemStatus.toUpperCase();
        }
    },

    // ----- LOG EKLE -----
    addLog: function(msg) {
        const logArea = document.getElementById('logArea');
        if (logArea) {
            logArea.innerHTML += `[${new Date().toLocaleTimeString()}] ${msg}<br>`;
            logArea.scrollTop = logArea.scrollHeight;
        }
        console.log(`📝 ${msg}`);
    },

    // ----- PERFORMANS METRİKLERİ -----
    getMetrics: function() {
        const active = this.state.agents.filter(a => a.aktif).length;
        return {
            totalAgents: this.state.agents.length,
            activeAgents: active,
            inactiveAgents: this.state.agents.length - active,
            systemStatus: this.state.systemStatus,
            cpuLoad: this.state.cpuLoad,
            lastUpdate: this.state.lastUpdate,
            isRunning: this.state.isRunning,
            safetyMode: this.state.safetyMode,
            metrics: this.state.metrics
        };
    },

    // ----- DEBUG MODU -----
    debug: function() {
        console.log("🐛 Orchestrator Debug Bilgileri:");
        console.log("State:", this.state);
        console.log("Ajanlar:", this.state.agents);
        console.log("Metrikler:", this.getMetrics());
        return this;
    }
};

// ----- ORCHESTRATOR'U GLOBAL HALE GETİR -----
window.Orchestrator = Orchestrator;

// ----- OTOMATİK BAŞLAT -----
if (document.readyState === 'complete') {
    Orchestrator.init();
} else {
    document.addEventListener('DOMContentLoaded', () => {
        Orchestrator.init();
    });
}

// ----- EKSİK FONKSİYONLAR İÇİN YEDEKLEME -----
if (typeof triggerEmergencyStop === 'undefined') {
    window.triggerEmergencyStop = function() {
        console.log("🚨 KRİZ PROTOKOLÜ - Orchestrator üzerinden durdurma");
        Orchestrator.stopSystem();
        
        if (typeof TRM_Gateway !== 'undefined' && TRM_Gateway.disconnectAll) {
            TRM_Gateway.disconnectAll();
        }
        
        if (typeof SosyalImece !== 'undefined' && SosyalImece.pauseDataSync) {
            SosyalImece.pauseDataSync();
        }
        
        alert("🚨 Sistem güvenli moda alındı. Tüm ajanlar durduruldu.");
    };
}

// ----- drawCPU İLE ENTEGRASYON -----
(function() {
    const originalDrawCPU = window.drawCPU;
    
    if (typeof originalDrawCPU === 'function') {
        window.drawCPU = function() {
            if (typeof originalDrawCPU === 'function') {
                originalDrawCPU();
            }
            
            if (typeof window.cpuLoad !== 'undefined') {
                Orchestrator.updateCPU(window.cpuLoad);
            }
        };
        console.log("✅ drawCPU override edildi - Orchestrator ile senkronize");
    } else {
        console.log("ℹ️ drawCPU fonksiyonu henüz tanımlanmamış, beklemede...");
        const checkInterval = setInterval(() => {
            if (typeof window.drawCPU === 'function' && window.drawCPU !== Orchestrator._wrappedDrawCPU) {
                const original = window.drawCPU;
                window.drawCPU = function() {
                    if (typeof original === 'function') original();
                    if (typeof window.cpuLoad !== 'undefined') {
                        Orchestrator.updateCPU(window.cpuLoad);
                    }
                };
                window._wrappedDrawCPU = window.drawCPU;
                clearInterval(checkInterval);
                console.log("✅ drawCPU başarıyla yakalandı ve Orchestrator ile senkronize edildi.");
            }
        }, 500);
        
        setTimeout(() => clearInterval(checkInterval), 10000);
    }
})();

console.log("🚀 Orchestrator v3.1 yüklendi ve hazır!");