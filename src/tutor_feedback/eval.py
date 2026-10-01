import json
from pathlib import Path
from time import perf_counter

from tutor_feedback.models import ReviewRequest
from tutor_feedback.reviewers import RuleReviewer


def run_eval(path: Path) -> dict[str, float | int]:
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    reviewer = RuleReviewer()
    exact = 0
    labels = 0
    elapsed_ms = 0.0
    for case in cases:
        start = perf_counter()
        result = reviewer.review(ReviewRequest(learner_text=case["input"]))
        elapsed_ms += (perf_counter() - start) * 1000
        exact += result.corrected_text == case["expected"]
        labels += set(case["issues"]).issubset({c.issue for c in result.corrections})
    count = len(cases)
    return {
        "cases": count,
        "exact_match_rate": round(exact / count, 3) if count else 0,
        "issue_recall_rate": round(labels / count, 3) if count else 0,
        "mean_latency_ms": round(elapsed_ms / count, 3) if count else 0,
    }


if __name__ == "__main__":
    fixture = Path(__file__).resolve().parents[2] / "evals" / "cases.jsonl"
    print(json.dumps(run_eval(fixture), indent=2))

