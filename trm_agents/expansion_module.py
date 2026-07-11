from trm_agents.Intelligence import build_market_intel_agents
from trm_agents.Network import build_bridge_agents
from trm_agents.Sentinel import build_sentinel_agents

BASELINE_AGENT_CAPACITY = 165


def build_expansion_agents():
    agent_specs = []

    for name, agent in build_market_intel_agents():
        agent_specs.append(
            {
                "name": name,
                "instance": agent,
                "capabilities": ["market_intelligence"],
                "context_allowlist": ["trend_report", "worker_mode", "active_agents"],
            }
        )

    for name, agent in build_bridge_agents():
        agent_specs.append(
            {
                "name": name,
                "instance": agent,
                "capabilities": ["affiliate_network_bridge"],
                "context_allowlist": ["trend_report", "worker_mode"],
            }
        )

    for name, agent in build_sentinel_agents():
        agent_specs.append(
            {
                "name": name,
                "instance": agent,
                "capabilities": ["sentinel_monitoring"],
                "context_allowlist": ["queue_payload", "poster_payload", "security_status", "worker_mode"],
            }
        )

    return agent_specs


def get_capacity_snapshot():
    market_count = 10
    bridge_count = 15
    sentinel_count = 10
    expansion_total = market_count + bridge_count + sentinel_count
    return {
        "baseline_agents": BASELINE_AGENT_CAPACITY,
        "market_intel_agents": market_count,
        "bridge_agents": bridge_count,
        "sentinel_agents": sentinel_count,
        "expansion_total": expansion_total,
        "total_capacity": BASELINE_AGENT_CAPACITY + expansion_total,
    }
