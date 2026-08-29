# Data Contracts

These data contracts are fixed and must not be redesigned.

## Scenario File
Location: `scenarios/*.json` (written by teammate's generator)

```json
{ 
  "id": "emi_017", 
  "method": "POST", 
  "path": "/api/emi",
  "body": {"principal": 500000, "annual_rate": 12, "months": 60},
  "tags": ["emi"] 
}
```

## Radius (Impact Step Output)

```json
{ 
  "changed": ["core/interest.py"],
  "affected_files": ["services/emi_service.py", "..."],
  "affected_endpoints": ["/api/emi", "/api/loan/{id}"],
  "call_paths": ["monthly_rate -> calculate_emi -> emi_endpoint"] 
}
```

## results.json (Replay Output)

```json
[ 
  { 
    "scenario": "emi_017",
    "old": {"status": 200, "json": {...}},
    "new": {"status": 200, "json": {...}} 
  } 
]
```

## report.json (Final Output)
Read by teammate's UI.

```json
{ 
  "summary": {
    "total": 58, 
    "identical": 55, 
    "intentional": 2,
    "regression": 1, 
    "unexplained": 0
  },
  "radius": { ...radius object... },
  "results": [ 
    { 
      "scenario": "emi_017", 
      "verdict": "regression",
      "diffs": [{"path": "emi", "old": 14820.0, "new": 10718.4}],
      "explanation": "one sentence",
      "rule": {"id": "D-17", "text": "...", "source": "PR #4"} 
    } 
  ] 
}
```
