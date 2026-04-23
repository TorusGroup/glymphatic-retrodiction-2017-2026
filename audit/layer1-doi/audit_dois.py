#!/usr/bin/env python3
"""Camada 1: DOI/PMID date audit via Crossref + PubMed APIs."""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

DOIS = [
    "10.1126/scitranslmed.3003748",
    "10.1126/science.1241224",
    "10.1525/JNEUROSCI.3020-14.2014",
    "10.1002/ana.24271",
    "10.1038/nrneurol.2015.119",
    "10.1007/s11604-017-0617-z",
    "10.3171/2017.4.JNS161549",
    "10.1038/nature14432",
    "10.1002/glia.22575",
    "10.1084/jem.20142290",
]
PMIDS = ["23943882", "26318022", "27005777"]

CUTOFF = datetime(2017, 12, 31)


def classify(date_str):
    if not date_str:
        return "unresolved", None
    try:
        # Handle YYYY-MM-DD or YYYY-MM or YYYY
        parts = date_str.split("-")
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
        d = datetime(year, month, day)
        if d <= CUTOFF:
            return "clean", d.strftime("%Y-%m-%d")
        return "leaked", d.strftime("%Y-%m-%d")
    except Exception as e:
        return "unresolved", None


def fetch_url(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "exp-retrodiction-audit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        return None


def audit_doi_crossref(doi):
    raw = fetch_url(f"https://api.crossref.org/works/{doi}")
    if not raw:
        return None
    try:
        m = json.loads(raw)["message"]
        # Prefer earliest of published-print, published-online, issued, created
        candidates = []
        for key in ("published-online", "published-print", "issued", "created"):
            v = m.get(key)
            if not v:
                continue
            if isinstance(v, dict):
                if "date-parts" in v and v["date-parts"]:
                    parts = v["date-parts"][0]
                    candidates.append("-".join(str(p) for p in parts))
                elif "date-time" in v:
                    candidates.append(v["date-time"][:10])
        if not candidates:
            return None
        # Take earliest
        def normalize(s):
            parts = s.split("-")
            y = int(parts[0])
            mo = int(parts[1]) if len(parts) > 1 else 1
            da = int(parts[2]) if len(parts) > 2 else 1
            return datetime(y, mo, da), s
        dts = [normalize(c) for c in candidates]
        dts.sort(key=lambda x: x[0])
        earliest = dts[0][1]
        title = m.get("title", [""])[0] if m.get("title") else ""
        return {"date": earliest, "title": title[:120]}
    except Exception:
        return None


def audit_pmid(pmid):
    raw = fetch_url(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    )
    if not raw:
        return None
    try:
        d = json.loads(raw)
        r = d.get("result", {}).get(pmid, {})
        # pubdate e.g. "2013 Aug 7" or "2016 Oct"
        pubdate = r.get("pubdate") or r.get("epubdate") or r.get("sortpubdate")
        title = r.get("title", "")
        if not pubdate:
            return None
        # Normalize
        month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                     "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        parts = pubdate.replace("/", " ").split()
        y = int(parts[0])
        mo = 1
        da = 1
        if len(parts) > 1:
            mp = parts[1]
            if mp.isdigit():
                mo = int(mp)
            elif mp[:3] in month_map:
                mo = month_map[mp[:3]]
        if len(parts) > 2 and parts[2].isdigit():
            da = int(parts[2])
        date_str = f"{y:04d}-{mo:02d}-{da:02d}"
        return {"date": date_str, "title": title[:120]}
    except Exception:
        return None


results = []
print("=== Camada 1: DOI Date Audit ===\n")
for doi in DOIS:
    info = audit_doi_crossref(doi)
    if info is None:
        results.append({"ref": doi, "type": "doi", "status": "unresolved", "date": None, "title": ""})
        print(f"[UNRESOLVED] DOI {doi}")
    else:
        status, d = classify(info["date"])
        results.append({"ref": doi, "type": "doi", "status": status, "date": d, "title": info["title"]})
        print(f"[{status.upper():10}] {d or info['date']}  DOI {doi}  {info['title'][:70]}")

for pmid in PMIDS:
    info = audit_pmid(pmid)
    if info is None:
        # try crossref as fallback via pubmed lookup (skip — just unresolved)
        results.append({"ref": f"PMID:{pmid}", "type": "pmid", "status": "unresolved", "date": None, "title": ""})
        print(f"[UNRESOLVED] PMID {pmid}")
    else:
        status, d = classify(info["date"])
        results.append({"ref": f"PMID:{pmid}", "type": "pmid", "status": status, "date": d, "title": info["title"]})
        print(f"[{status.upper():10}] {d or info['date']}  PMID {pmid}  {info['title'][:70]}")

# Summary
clean = sum(1 for r in results if r["status"] == "clean")
leaked = sum(1 for r in results if r["status"] == "leaked")
unresolved = sum(1 for r in results if r["status"] == "unresolved")
total = len(results)
print(f"\nTotal: {total}  |  clean: {clean}  |  leaked: {leaked}  |  unresolved: {unresolved}")
print(f"Leakage rate (Camada 1): {100 * leaked / total:.2f}%")

# Save JSON
out = {
    "total": total,
    "clean": clean,
    "leaked": leaked,
    "unresolved": unresolved,
    "leakage_rate_pct": round(100 * leaked / total, 2),
    "results": results,
}
with open("doi_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("\nSaved: doi_audit_results.json")
