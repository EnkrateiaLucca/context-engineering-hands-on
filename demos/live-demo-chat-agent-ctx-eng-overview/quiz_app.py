# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic", "fastapi", "uvicorn", "python-dotenv"]
# ///
"""
Quiz App — a tiny chat-driven quiz generator.

Run:  uv run quiz_app.py
Then open: http://127.0.0.1:8501

This builds on structured_output_example.py: the user types a topic into a
little chat box, we ask Claude for a Quiz via `messages.parse` (structured
output), dynamically render the questions in the browser, and score the
answers once submitted.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

import anthropic
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

MODEL = "claude-sonnet-4-6"

client = anthropic.Anthropic()
app = FastAPI()


# ─── STRUCTURED OUTPUT SCHEMA ─────────────────────────────────────
# Same idea as structured_output_example.py's `Quiz`, extended to
# multiple-choice so we can render options and auto-grade the result.
class Question(BaseModel):
    question: str
    options: list[str] = Field(description="Exactly 4 answer choices")
    correct_index: int = Field(description="0-based index of the correct option")
    explanation: str = Field(description="One sentence on why that answer is correct")


class Quiz(BaseModel):
    title: str
    questions: list[Question]
# ──────────────────────────────────────────────────────────────────


@app.post("/api/quiz")
async def generate_quiz(request: Request):
    body = await request.json()
    topic = (body.get("topic") or "").strip()
    num = int(body.get("num_questions") or 3)

    if not topic:
        return JSONResponse({"error": "Please describe a quiz topic."}, status_code=400)

    user_input = (
        f"Create a multiple-choice quiz about: {topic}.\n"
        f"{num} questions. Each question has exactly 4 options with one correct answer."
    )

    response = client.messages.parse(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": user_input}],
        output_format=Quiz,
    )

    return JSONResponse(response.parsed_output.model_dump())


@app.get("/")
async def index():
    return HTMLResponse(PAGE)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Quiz Bot</title>
<style>
  :root {
    --bg: #0f1115; --panel: #171a21; --ink: #e8eaed; --muted: #9aa0aa;
    --accent: #6ea8fe; --good: #34d399; --bad: #f87171; --line: #262b34;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--ink);
    font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    display: flex; justify-content: center; padding: 32px 16px;
  }
  .wrap { width: 100%; max-width: 680px; }
  h1 { font-size: 22px; margin: 0 0 4px; }
  .sub { color: var(--muted); margin: 0 0 24px; }
  .chat {
    background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
    padding: 16px; display: flex; gap: 10px; align-items: center;
  }
  .chat input[type=text] {
    flex: 1; background: #0c0e12; border: 1px solid var(--line); color: var(--ink);
    padding: 12px 14px; border-radius: 10px; font-size: 15px; outline: none;
  }
  .chat input[type=text]:focus { border-color: var(--accent); }
  .chat select {
    background: #0c0e12; border: 1px solid var(--line); color: var(--ink);
    padding: 12px 8px; border-radius: 10px;
  }
  button {
    background: var(--accent); color: #08131f; border: 0; font-weight: 600;
    padding: 12px 18px; border-radius: 10px; cursor: pointer; font-size: 15px;
  }
  button:disabled { opacity: .5; cursor: default; }
  .hint { color: var(--muted); font-size: 13px; margin: 10px 2px 0; }
  .hint code { background: #0c0e12; padding: 2px 6px; border-radius: 6px; }
  .card {
    background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
    padding: 18px 20px; margin-top: 16px;
  }
  .q-title { font-weight: 600; margin: 0 0 12px; }
  .opt {
    display: block; border: 1px solid var(--line); border-radius: 10px;
    padding: 11px 14px; margin: 8px 0; cursor: pointer; transition: .12s;
  }
  .opt:hover { border-color: var(--accent); }
  .opt input { margin-right: 10px; }
  .opt.correct { border-color: var(--good); background: rgba(52,211,153,.08); }
  .opt.wrong { border-color: var(--bad); background: rgba(248,113,113,.08); }
  .explain { color: var(--muted); font-size: 13px; margin-top: 10px; display: none; }
  .explain.show { display: block; }
  .score {
    text-align: center; font-size: 20px; font-weight: 700; padding: 20px;
    background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
    margin-top: 16px;
  }
  .loading { color: var(--muted); text-align: center; padding: 24px; }
  .row { display: flex; gap: 10px; margin-top: 18px; }
  .ghost { background: transparent; border: 1px solid var(--line); color: var(--ink); }
</style>
</head>
<body>
<div class="wrap">
  <h1>🧠 Quiz Bot</h1>
  <p class="sub">Tell the bot what to quiz you on. It builds the questions on the fly.</p>

  <div class="chat">
    <input id="topic" type="text" placeholder="e.g. Python basics for automation"
           autocomplete="off" />
    <select id="num">
      <option value="3">3 Qs</option>
      <option value="5">5 Qs</option>
      <option value="8">8 Qs</option>
    </select>
    <button id="go">Generate</button>
  </div>
  <p class="hint">Try: <code>context windows &amp; token budgets</code>,
     <code>git rebase</code>, <code>the four context failure modes</code></p>

  <div id="out"></div>
</div>

<script>
const topicEl = document.getElementById('topic');
const numEl = document.getElementById('num');
const goEl = document.getElementById('go');
const out = document.getElementById('out');
let quiz = null;

async function generate() {
  const topic = topicEl.value.trim();
  if (!topic) { topicEl.focus(); return; }
  goEl.disabled = true;
  out.innerHTML = '<div class="loading">Building your quiz…</div>';
  try {
    const res = await fetch('/api/quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, num_questions: Number(numEl.value) })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Something went wrong.');
    quiz = data;
    renderQuiz();
  } catch (e) {
    out.innerHTML = '<div class="loading">⚠️ ' + e.message + '</div>';
  } finally {
    goEl.disabled = false;
  }
}

function renderQuiz() {
  let html = '<h2 style="margin:22px 2px 4px">' + escapeHtml(quiz.title) + '</h2>';
  quiz.questions.forEach((q, qi) => {
    html += '<div class="card" data-q="' + qi + '"><p class="q-title">' +
            (qi + 1) + '. ' + escapeHtml(q.question) + '</p>';
    q.options.forEach((opt, oi) => {
      html += '<label class="opt" data-opt="' + oi + '">' +
              '<input type="radio" name="q' + qi + '" value="' + oi + '">' +
              escapeHtml(opt) + '</label>';
    });
    html += '<p class="explain">' + escapeHtml(q.explanation) + '</p></div>';
  });
  html += '<div class="row">' +
          '<button id="submit">Submit answers</button>' +
          '<button id="reset" class="ghost">New quiz</button></div>';
  out.innerHTML = html;
  document.getElementById('submit').onclick = grade;
  document.getElementById('reset').onclick = () => {
    out.innerHTML = ''; topicEl.value = ''; topicEl.focus();
  };
}

function grade() {
  let score = 0;
  quiz.questions.forEach((q, qi) => {
    const card = out.querySelector('[data-q="' + qi + '"]');
    const picked = card.querySelector('input[name="q' + qi + '"]:checked');
    const chosen = picked ? Number(picked.value) : -1;
    if (chosen === q.correct_index) score++;
    card.querySelectorAll('.opt').forEach((el) => {
      const oi = Number(el.dataset.opt);
      el.querySelector('input').disabled = true;
      if (oi === q.correct_index) el.classList.add('correct');
      else if (oi === chosen) el.classList.add('wrong');
    });
    card.querySelector('.explain').classList.add('show');
  });
  const total = quiz.questions.length;
  const pct = Math.round((score / total) * 100);
  const banner = document.createElement('div');
  banner.className = 'score';
  banner.textContent = 'You scored ' + score + ' / ' + total + '  (' + pct + '%)';
  out.prepend(banner);
  document.getElementById('submit').disabled = true;
  banner.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

goEl.onclick = generate;
topicEl.addEventListener('keydown', e => { if (e.key === 'Enter') generate(); });
topicEl.focus();
</script>
</body>
</html>"""


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY (or put it in a .env file) first.")
    uvicorn.run(app, host="127.0.0.1", port=8501)
