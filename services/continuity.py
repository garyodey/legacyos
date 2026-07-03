from services.store import store


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def memory_score() -> float:
    recorded_memories = sum(1 for m in store.memory if m.get("recorded"))
    total_memories = max(len(store.memory), 1)
    memory_recording = (recorded_memories / total_memories) * 100
    people_depth = min(len(store.people) * 8, 100)
    land_depth = min(len(store.land) * 20, 100)
    return round(clamp((memory_recording * 0.5) + (people_depth * 0.25) + (land_depth * 0.25)), 2)


def adaptive_score() -> float:
    remittance_depth = min(len(store.remittances) * 20, 100)
    surveyed = sum(1 for l in store.land if str(l.get("survey_status", "")).lower() in ["available", "complete", "yes"])
    land_total = max(len(store.land), 1)
    document_proxy = (surveyed / land_total) * 100
    return round(clamp((remittance_depth * 0.4) + (document_proxy * 0.4) + 20), 2)


def erosion_score() -> float:
    severity_points = {"Low": 10, "Medium": 25, "High": 45, "Critical": 65}
    raw = 25
    for r in store.risks:
        raw += severity_points.get(r.get("severity", "Medium"), 25) / 4
    recorded_memories = sum(1 for m in store.memory if m.get("recorded"))
    raw -= recorded_memories * 5
    return round(clamp(raw, 10, 100), 2)


def state_from_ci(ci: float) -> str:
    if ci > 140:
        return "Alpha"
    if ci >= 100:
        return "Beta"
    if ci >= 60:
        return "Gamma"
    return "Delta"


def calculate_continuity_score():
    mem = memory_score()
    ada = adaptive_score()
    ero = erosion_score()
    ci = round((mem * ada) / max(ero, 1), 2)
    return {
        "memory_score": mem,
        "adaptive_score": ada,
        "erosion_score": ero,
        "continuity_index": ci,
        "state": state_from_ci(ci),
    }


def recommend_interventions():
    score = calculate_continuity_score()
    interventions = []
    unrecorded = [m for m in store.memory if not m.get("recorded")]
    if unrecorded:
        interventions.append({
            "priority": "Critical",
            "action": "Record elder interviews within 30 days.",
            "reason": f"{len(unrecorded)} memory record(s) remain unrecorded.",
        })
    pending_land = [l for l in store.land if str(l.get("survey_status", "")).lower() not in ["available", "complete", "yes"]]
    if pending_land:
        interventions.append({
            "priority": "High",
            "action": "Digitize and verify land/property records.",
            "reason": f"{len(pending_land)} land/property record(s) lack complete survey status.",
        })
    if score["state"] in ["Gamma", "Delta"]:
        interventions.append({
            "priority": "Critical",
            "action": "Hold a family continuity meeting immediately.",
            "reason": f"Continuity state is {score['state']}.",
        })
    if not interventions:
        interventions.append({
            "priority": "Normal",
            "action": "Maintain archive updates and schedule annual family continuity review.",
            "reason": f"Continuity state is {score['state']}.",
        })
    return interventions
