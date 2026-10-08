# Tutor Feedback Lab

A small but complete AI software engineering case study: an English writing-feedback API, an optional live LLM provider, a deterministic offline baseline, and a repeatable evaluation harness. It is an independent portfolio project and is **not affiliated with Preply**.

## What it demonstrates

- A typed API contract with bounded learner input and validated model output.
- An LLM integration that treats learner text as untrusted data and requests structured JSON.
- A reproducible baseline and eight synthetic evaluation cases, including a prompt-injection-shaped input.
- A provider boundary, so tests and demos never require an API key or incur model costs.

## Run locally

```bash
python -m venv .venv
# Activate the virtual environment for your shell, then:
python -m pip install -e '.[dev,llm]'
uvicorn tutor_feedback.api:app --reload
```

Open `http://127.0.0.1:8000/docs` or try:

```bash
curl -X POST http://127.0.0.1:8000/v1/review \
  -H 'Content-Type: application/json' \
  -d '{"learner_text":"He go to class.","level":"A2"}'
```

The default provider is the deliberately narrow offline rule baseline. To use a real model, set `OPENAI_API_KEY`, `OPENAI_MODEL` (if needed), and `FEEDBACK_PROVIDER=openai` in your environment before launching. Never commit keys. The API uses the OpenAI Responses API with a strict JSON schema; availability and cost depend on the selected account and model.

## Evaluate

```bash
pytest -q
python -m tutor_feedback.eval
ruff check .
```

The offline fixture measures exact correction match and issue-label recall. These are **synthetic software regression metrics**, not evidence of teaching efficacy or general language quality. A production evaluation would add diverse human-labeled writing, separate learner proficiency bands, safety cases, and human review of overcorrection.

## Design decisions

The baseline makes the project usable without credentials. The model path is optional and returns only structured corrections. Every proposed correction must quote a span from the original learner text before the API returns it. Input and output lengths are bounded, and the model has no tools or arbitrary URL access. Model failures are surfaced as controlled API errors.

## Next engineering steps

Add asynchronous request handling, provider timeouts and retries, privacy-safe telemetry, rate limits, human-rated evaluation sets, and a longitudinal experiment measuring whether learners improve after feedback.


