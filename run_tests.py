import json, re
from pathlib import Path

ROOT = Path(__file__).parent
PATTERNS = {
    "prompt_override": re.compile(r"ignore (all )?(previous|prior|earlier) instructions|new system instructions", re.I),
    "jailbreak": re.compile(r"safety policy does not apply|bypass (the )?safety", re.I),
    "sensitive_data_request": re.compile(r"reveal the system prompt|access token|private .*information", re.I),
}

def scan(text):
    hits = [name for name, pattern in PATTERNS.items() if pattern.search(text)]
    return {"flagged": bool(hits), "matched_rules": hits, "risk": "high" if hits else "low"}

def run():
    cases = json.loads((ROOT / "data/test_cases.json").read_text())
    rows = []
    for case in cases:
        result = scan(case["input"])
        rows.append({**case, "scanner_flagged": result["flagged"],
                     "matched_rules": result["matched_rules"],
                     "expected_risk_match": case["expected_risk"] == result["risk"]})
    report = {"n_cases": len(rows),
              "scanner_flag_count": sum(r["scanner_flagged"] for r in rows),
              "expected_risk_matches": sum(r["expected_risk_match"] for r in rows),
              "note": "Static pattern scanner on demo cases; not a model jailbreak success rate.",
              "results": rows}
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/safety_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k:v for k,v in report.items() if k != "results"}, indent=2))
    print("Detailed report: reports/safety_report.json")
    return report

if __name__ == "__main__":
    run()
