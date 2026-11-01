# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-cellular-dna-damage-gamma-h2ax-foci-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_gamma_h2ax_dna_damage_foci(mean_foci_per_cell, age_years, previous_foci=None, recent_radiation_exposure=False):
    if mean_foci_per_cell < 0 or age_years <= 0:
        raise ValueError("Foci count must be non-negative and age must be positive")
        
    # Baseline normal gamma-H2AX in healthy lymphocytes:
    # Young adults (< 40): 0.05 - 0.15 foci/cell
    # Middle age (40 - 65): 0.15 - 0.35 foci/cell
    # Elderly (> 65): 0.30 - 0.55 foci/cell
    # Severe genotoxic damage / radiomimetic stress: > 0.80 foci/cell
    expected_foci = 0.08 + (0.005 * (age_years - 20.0)) if age_years > 20 else 0.08
    delta_foci = mean_foci_per_cell - expected_foci
    
    if mean_foci_per_cell > 0.70:
        tier = "CRITICAL_DOUBLE_STRAND_BREAK_BURDEN"
        action = "High genomic instability; evaluate recent CT scans, flight radiation, or environmental genotoxins."
    elif mean_foci_per_cell > 0.35:
        tier = "MODERATE_ACCUMULATED_DNA_DAMAGE"
        action = "Elevated un-repaired DNA breaks; support PARP/SIRT pathways with NAD+ precursors and antioxidants."
    else:
        tier = "MINIMAL_GENOMIC_INTEGRITY_PRESERVED"
        action = "Intact homologous recombination / NHEJ DNA repair capacity."
        
    repair_capacity_compromised = delta_foci > 0.25
    
    return {
        "mean_gamma_h2ax_foci_per_cell": round(mean_foci_per_cell, 3),
        "expected_baseline_for_age": round(expected_foci, 3),
        "delta_excess_foci": round(delta_foci, 3),
        "genomic_damage_tier": tier,
        "impaired_dna_repair_flag": repair_capacity_compromised,
        "clinical_action_plan": action
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_gamma_h2ax_dna_damage_foci",
                        "description": """Quantify cellular genomic instability and double-strand DNA breaks (DSBs) using phosphorylated histone gamma-H2AX foci per lymphocyte.
Evaluates baseline genotoxic stress, radiation exposure burden, DNA damage repair kinetics, and premature aging vulnerability.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_gamma_h2ax_dna_damage_foci(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'mean_foci_per_cell': 0.42, 'age_years': 46, 'previous_foci': 0.28, 'recent_radiation_exposure': False}
        out = audit_gamma_h2ax_dna_damage_foci(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
