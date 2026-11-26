#!/usr/bin/env python3
"""Compare a saved draft with the reply the owner actually sent.

Deterministic, no network. Reads a JSON array on stdin (or a file path as the
first argument) of objects:

    {"id": "...", "audience": "...", "draft": "<draft body>", "sent": "<sent body>"}

`sent` may be null when the draft was discarded. Writes a JSON array with one
result per input:

    {"id", "audience", "verdict", "draft_words", "sent_words", "length_ratio",
     "similarity", "greeting": [draft, sent], "signoff": [draft, sent],
     "removed": [...sentences], "added": [...sentences]}

verdict is one of: unchanged, light_edit, heavy_edit, rewrite, discarded.

Both bodies are cleaned the same way first: quoted history ("On ... wrote:",
lines starting with ">") and the signature block are cut. Pass
--sig-start REGEX (repeatable) for signature first-lines that are not the
standard "-- " delimiter.
"""

import argparse
import difflib
import json
import re
import sys
import unicodedata

QUOTE = re.compile(
    r"(?m)^(On .{5,200}wrote:|-{2,}\s*Original Message|From: .+\nSent: |_{5,}|-{5,} Forwarded)"
)
SIGNOFF = re.compile(
    r"(?i)^(best|thanks|thank you|thx|regards|best regards|cheers|warmly|talk soon)\b[^\n]{0,20}$"
)
GREETING = re.compile(r"^(?i:hi|hey|hello|dear|good (?:morning|afternoon))\b[^\n,]{0,30},?|^[A-Z][\w'-]+,(?=\s|$)")


def clean(text, sig_patterns):
    if not text:
        return ""
    t = text.replace("\r", "")
    # Client-inserted HTML signature and quote containers (Gmail, Apple Mail, Outlook).
    # Attribute markers cut at the start of the tag that carries them; a <blockquote> cuts at itself,
    # so reply text in the same container survives.
    cuts = []
    for marker in ('class="gmail_signature"', 'class="gmail_quote"', 'id="Signature"'):
        i = t.find(marker)
        if i >= 0:
            j = t.rfind("<", 0, i)
            cuts.append(j if j >= 0 else i)
    i = t.lower().find("<blockquote")
    if i >= 0:
        cuts.append(i)
    if cuts:
        t = t[: min(cuts)]
    if "<" in t and ">" in t and re.search(r"(?i)</?(p|div|br|html|body)\b", t):
        t = re.sub(r"(?is)<(script|style|head).*?</\1>", "", t)
        t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>", "\n", t)
        t = re.sub(r"<[^>]+>", "", t)
        import html

        t = html.unescape(t)
    m = QUOTE.search(t)
    if m:
        t = t[: m.start()]
    lines = [l for l in t.split("\n") if not l.lstrip().startswith(">")]
    cut = len(lines)
    for i, l in enumerate(lines):
        s = l.strip()
        if s == "--" or l.startswith("-- ") or any(p.search(s) for p in sig_patterns):
            cut = i
            break
    return "\n".join(lines[:cut]).strip()


def first_line(t):
    for l in t.split("\n"):
        if l.strip():
            return l.strip()
    return ""


def greeting(t):
    fl = first_line(t)
    m = GREETING.match(fl)
    if not m or re.match(r"(?i)(thanks|thank|thx|yes|no|ok|okay|sure|sorry|great|perfect)\b", fl):
        return "none"
    return m.group(0).strip()


def signoff(t):
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    for i in range(len(lines) - 1, max(-1, len(lines) - 4), -1):
        if SIGNOFF.match(lines[i]):
            return " ".join(lines[i : i + 2])
    return "none"


def sentences(t):
    flat = re.sub(r"\s+", " ", t).strip()
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p.strip() for p in parts if len(p.split()) >= 3]


def norm(s):
    # Keep letters, combining marks and digits in any script, and spaces; drop everything else.
    return "".join(c for c in s.lower() if c == " " or unicodedata.category(c)[0] in "LMN")


def compare(item, sig_patterns):
    draft = clean(item.get("draft", ""), sig_patterns)
    sent_raw = item.get("sent")
    out = {"id": item.get("id"), "audience": item.get("audience")}
    dw = len(draft.split())
    out["draft_words"] = dw
    if sent_raw is None:
        out.update(verdict="discarded", sent_words=0)
        return out
    sent = clean(sent_raw, sig_patterns)
    sw = len(sent.split())
    sim = difflib.SequenceMatcher(None, norm(draft), norm(sent), autojunk=False).ratio()
    ds, ss = sentences(draft), sentences(sent)
    dn, sn = {norm(s) for s in ds}, {norm(s) for s in ss}
    removed = [s for s in ds if norm(s) not in sn and max((difflib.SequenceMatcher(None, norm(s), x, autojunk=False).ratio() for x in sn), default=0) < 0.6]
    added = [s for s in ss if norm(s) not in dn and max((difflib.SequenceMatcher(None, norm(s), x, autojunk=False).ratio() for x in dn), default=0) < 0.6]
    if sim >= 0.97:
        verdict = "unchanged"
    elif sim >= 0.8:
        verdict = "light_edit"
    elif sim >= 0.4:
        verdict = "heavy_edit"
    else:
        verdict = "rewrite"
    out.update(
        verdict=verdict,
        sent_words=sw,
        length_ratio=round(sw / dw, 2) if dw else None,
        similarity=round(sim, 3),
        greeting=[greeting(draft), greeting(sent)],
        signoff=[signoff(draft), signoff(sent)],
        removed=removed[:12],
        added=added[:12],
    )
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", nargs="?", help="JSON file; default stdin")
    ap.add_argument("--sig-start", action="append", default=[], help="regex for a signature's first line")
    a = ap.parse_args()
    data = json.load(open(a.path) if a.path else sys.stdin)
    pats = [re.compile(p) for p in a.sig_start]
    json.dump([compare(x, pats) for x in data], sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
