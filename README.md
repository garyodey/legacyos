# LegacyOS v10 Backend

FastAPI prototype for the LegacyOS Continuity Intelligence Engine.

## Run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Core endpoints

- `GET /health`
- `POST /person`
- `POST /land`
- `POST /memory`
- `POST /risk`
- `POST /remittance`
- `GET /continuity_score`
- `GET /interventions`

## Continuity formula

```text
Continuity Index = (Memory Score × Adaptive Score) ÷ Identity Erosion Score
```

States:

- Alpha: CI > 140
- Beta: 100–140
- Gamma: 60–99
- Delta: < 60
