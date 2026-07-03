from fastapi import FastAPI
from models import Person, Land, MemoryRecord, Risk, Remittance, ContinuityScore, Intervention
from services.store import store
from services.continuity import calculate_continuity_score, recommend_interventions

app = FastAPI(
    title="LegacyOS v10 Backend",
    description="Continuity Intelligence Engine prototype for family memory, assets, risk, and interventions.",
    version="10.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "system": "LegacyOS v10"}


@app.post("/person")
def create_person(person: Person):
    return store.add("people", person.model_dump())


@app.post("/land")
def create_land(land: Land):
    return store.add("land", land.model_dump())


@app.post("/memory")
def create_memory(memory: MemoryRecord):
    return store.add("memory", memory.model_dump())


@app.post("/risk")
def create_risk(risk: Risk):
    return store.add("risks", risk.model_dump())


@app.post("/remittance")
def create_remittance(remittance: Remittance):
    return store.add("remittances", remittance.model_dump())


@app.get("/continuity_score", response_model=ContinuityScore)
def continuity_score():
    return calculate_continuity_score()


@app.get("/interventions", response_model=list[Intervention])
def interventions():
    return recommend_interventions()


@app.get("/snapshot")
def snapshot():
    return {
        "people": store.people,
        "land": store.land,
        "memory": store.memory,
        "risks": store.risks,
        "remittances": store.remittances,
        "score": calculate_continuity_score(),
        "interventions": recommend_interventions(),
    }
