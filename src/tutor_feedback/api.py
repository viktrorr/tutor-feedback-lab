import os

from fastapi import FastAPI, HTTPException

from tutor_feedback.models import ReviewRequest, ReviewResult
from tutor_feedback.reviewers import OpenAIReviewer, Reviewer, RuleReviewer


def create_app(reviewer: Reviewer | None = None) -> FastAPI:
    selected = reviewer or (
        OpenAIReviewer() if os.environ.get("FEEDBACK_PROVIDER") == "openai" else RuleReviewer()
    )
    app = FastAPI(title="Tutor Feedback Lab", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/review", response_model=ReviewResult)
    def review(request: ReviewRequest) -> ReviewResult:
        try:
            return selected.review(request)
        except ValueError as exc:
            raise HTTPException(status_code=502, detail="Feedback validation failed") from exc

    return app


app = create_app()

