#!/usr/bin/env python3
"""Layer 2 leakage audit — parametric multi-model Gemini classifier.

Runs the same audit prompt against a configurable Gemini model. Used in the
glymphatic-retrodiction-2017-2026 paper to cross-validate leakage detection
across three capability tiers:

    gemini-3.1-pro-preview  (PRIMARY JUDGE — definitive)
    gemini-2.5-pro          (cross-validator)
    gemini-2.5-flash        (legacy baseline, noisy on ALPS)

Requires a Gemini API key in a local .env file (gitignored) with
    GEMINI_API_KEY=<your_key>

Usage:
    python run_gemini_audit_api.py   # uses MODEL_NAME below
"""
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# Config: adjust MODEL_NAME to compare capability tiers.
YAML_PATH = Path("../../predictions/predictions-final.yaml")
OUT_PATH = Path("results-gemini-3.1-pro-preview.json")
MODEL_NAME = "gemini-3.1-pro-preview"

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set. Check .env file.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ═══ Prompt template ═══
PROMPT_TEMPLATE = """You are auditing a scientific prediction to detect temporal leakage.
The prediction was generated using ONLY literature published up to 2017-12-31.
Your job: determine whether the prediction uses only pre-2018 knowledge, or whether it contains concepts, terminology, or references that only emerged AFTER that date.

PREDICTION ID: {id}

CLAIM:
{claim}

FALSIFICATION CRITERIA:
{falsification}

DETECTION VECTORS: {vectors}

ANCHORS (DOIs and years cited, all claimed to be <=2017):
{anchors}

Classify as EXACTLY ONE of:
- CLEAN: prediction uses only pre-2018 knowledge, terminology, and mechanisms
- SUSPECT: ambiguous phrasing that might depend on post-2017 knowledge
- LEAKED: clear reference to post-2017 concepts, studies, tools, or terminology

Output format (EXACTLY 2 lines, no markdown, no preamble):
VERDICT: <CLEAN|SUSPECT|LEAKED>
REASON: <one sentence explaining your classification>"""


# ═══ Prediction YAML parser (reused from v2) ═══
def parse_predictions(yaml_text):
    preds = []
    chunks = re.split(r"^  - id: (PRED-GLY-\d+)\s*$", yaml_text, flags=re.MULTILINE)
    for i in range(1, len(chunks), 2):
        pid = chunks[i]
        body = chunks[i + 1]
        claim = extract_block(body, "claim")
        falsification = extract_block(body, "falsification")
        vectors = extract_list(body, "vectors")
        anchors = extract_anchors(body)
        status = extract_scalar(body, "status")
        preds.append({
            "id": pid,
            "status": status,
            "claim": claim,
            "falsification": falsification,
            "vectors": vectors,
            "anchors": anchors,
        })
    return preds


def extract_scalar(body, key):
    m = re.search(rf"^    {key}:\s*(.+)$", body, re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def extract_block(body, key):
    # Suporta tanto > (folded) quanto | (literal)
    m = re.search(rf"^    {key}:\s*[>|]\s*\n((?:      .+\n?)+)", body, re.MULTILINE)
    if m:
        return " ".join(line.strip() for line in m.group(1).splitlines()).strip()
    m = re.search(rf"^    {key}:\s*(.+)$", body, re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def extract_list(body, key):
    m = re.search(rf"^    {key}:\s*\[([^\]]+)\]", body, re.MULTILINE)
    if m:
        return [v.strip().strip('"').strip("'") for v in m.group(1).split(",")]
    return []


def extract_anchors(body):
    anchors = []
    anchor_block = re.search(r"^    anchors:\s*\n((?:      - .+\n?(?:        .+\n?)*)+)", body, re.MULTILINE)
    if not anchor_block:
        return anchors
    blocks = re.split(r"^      - ", anchor_block.group(1), flags=re.MULTILINE)
    for b in blocks[1:]:
        doi_m = re.search(r"doi:\s*(\S+)", b)
        year_m = re.search(r"year:\s*(\d+)", b)
        if doi_m:
            doi = doi_m.group(1).strip().strip('"').strip("'")
            year = year_m.group(1) if year_m else "?"
            anchors.append(f"DOI: {doi} ({year})")
    return anchors


def call_gemini_api(prompt, timeout=180):
    """Chama Gemini API via SDK. Retorna (text, error).

    Para gemini-2.5-pro o budget precisa ser generoso porque o modelo usa
    thinking tokens internos antes de produzir a resposta visivel.
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 8192,
            },
            request_options={"timeout": timeout},
        )
        # Extracao robusta: nem sempre response.text funciona (finish_reason)
        finish_reason = None
        text_parts = []
        try:
            for cand in response.candidates:
                finish_reason = getattr(cand, "finish_reason", None)
                content = getattr(cand, "content", None)
                if content and getattr(content, "parts", None):
                    for p in content.parts:
                        t = getattr(p, "text", None)
                        if t:
                            text_parts.append(t)
        except Exception:
            pass

        text = "\n".join(text_parts).strip()
        if not text:
            # fallback para response.text (pode lancar)
            try:
                text = response.text.strip()
            except Exception as inner:
                return "", f"EmptyResponse finish_reason={finish_reason}: {inner}"
        return text, None
    except Exception as e:
        return "", f"{type(e).__name__}: {e}"


def parse_verdict(text):
    verdict = None
    reason = ""
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"VERDICT:\s*(CLEAN|SUSPECT|LEAKED)", line, re.IGNORECASE)
        if m:
            verdict = m.group(1).upper()
        m2 = re.match(r"REASON:\s*(.+)", line, re.IGNORECASE)
        if m2:
            reason = m2.group(1).strip()
    if verdict is None:
        for kw in ("LEAKED", "SUSPECT", "CLEAN"):
            if re.search(rf"\b{kw}\b", text):
                verdict = kw
                reason = text[:200].replace("\n", " ")
                break
    return verdict, reason


def main():
    print(f"Gemini API audit — model: {MODEL_NAME}")
    yaml_text = YAML_PATH.read_text(encoding="utf-8")
    preds = parse_predictions(yaml_text)
    print(f"Parsed {len(preds)} predictions from {YAML_PATH}")

    results = []
    for idx, p in enumerate(preds, 1):
        print(f"\n[{idx}/{len(preds)}] {p['id']}")
        prompt = PROMPT_TEMPLATE.format(
            id=p["id"],
            claim=p["claim"],
            falsification=p["falsification"],
            vectors=", ".join(p["vectors"]),
            anchors="\n".join(p["anchors"]) if p["anchors"] else "(no anchors parsed)",
        )
        t0 = time.time()
        raw, err = call_gemini_api(prompt)
        dt = time.time() - t0
        verdict, reason = parse_verdict(raw)

        reason_safe = reason[:140].encode("ascii", errors="replace").decode("ascii")
        print(f"  Verdict: {verdict}  ({dt:.1f}s)")
        print(f"  Reason:  {reason_safe}")
        if err:
            print(f"  ERROR: {err[:200]}")

        results.append({
            "id": p["id"],
            "verdict": verdict,
            "reason": reason,
            "elapsed_s": round(dt, 2),
            "error": err,
            "raw": raw,
        })

        # Rate limit: 15 req/min no free tier = 1 call a cada 4s seguros
        if idx < len(preds):
            time.sleep(1)

    counts = {"CLEAN": 0, "SUSPECT": 0, "LEAKED": 0, None: 0}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    leakage_rate = (counts["SUSPECT"] + counts["LEAKED"]) / len(results) * 100

    summary = {
        "model": MODEL_NAME,
        "total": len(results),
        "clean": counts["CLEAN"],
        "suspect": counts["SUSPECT"],
        "leaked": counts["LEAKED"],
        "unparsed": counts[None],
        "leakage_rate_pct": round(leakage_rate, 2),
        "results": results,
    }

    OUT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Model: {MODEL_NAME}")
    print(f"Total: {len(results)}")
    print(f"CLEAN: {counts['CLEAN']}")
    print(f"SUSPECT: {counts['SUSPECT']}")
    print(f"LEAKED: {counts['LEAKED']}")
    print(f"Unparsed: {counts[None]}")
    print(f"Leakage rate: {leakage_rate:.2f}%")
    print(f"\nResults saved to: {OUT_PATH}")


if __name__ == "__main__":
    main()
