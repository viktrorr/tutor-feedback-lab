from typing import Literal

from pydantic import BaseModel, Field, model_validator

Level = Literal["A1", "A2", "B1", "B2", "C1", "C2"]
Issue = Literal["agreement", "verb_form", "word_choice", "other"]


class ReviewRequest(BaseModel):
    learner_text: str = Field(min_length=1, max_length=600)
    target_language: Literal["en"] = "en"
    level: Level = "B1"
    task_context: str = Field(default="", max_length=300)

    @model_validator(mode="after")
    def reject_blank_text(self) -> "ReviewRequest":
        if not self.learner_text.strip():
            raise ValueError("learner_text must contain visible text")
        return self


class Correction(BaseModel):
    original: str = Field(min_length=1, max_length=120)
    replacement: str = Field(min_length=1, max_length=120)
    issue: Issue
    explanation: str = Field(min_length=1, max_length=240)


class ReviewResult(BaseModel):
    corrected_text: str = Field(min_length=1, max_length=900)
    corrections: list[Correction] = Field(max_length=8)
    encouragement: str = Field(min_length=1, max_length=180)
    provider: Literal["rules", "openai"]


def validate_review(request: ReviewRequest, result: ReviewResult) -> ReviewResult:
    """Reject malformed model output before it reaches an API consumer."""
    if not result.corrected_text.strip():
        raise ValueError("corrected_text is blank")
    for correction in result.corrections:
        if correction.original.casefold() not in request.learner_text.casefold():
            raise ValueError("a correction does not quote the learner's text")
    return result

