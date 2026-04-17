# -*- coding: utf-8 -*-
"""Format PDF-extracted paper.md: hyphenation, noise removal, Markdown structure."""
import re
import sys

NOISE_PREFIXES = (
    "LADC 2022, November",
    "Partitioned State Machine Replication LADC",
)


def is_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    for p in NOISE_PREFIXES:
        if s.startswith(p):
            return True
    if "ACM ISBN 978" in s:
        return True
    if s.startswith("https://doi.org/10.1145/nnnnnnn"):
        return True
    return False


def fix_hyphenation(text: str) -> str:
    return re.sub(r"([a-zA-Z])-\n([a-zA-Z])", r"\1\2", text)


def fix_spaces(text: str) -> str:
    text = re.sub(r"InProceedings", "In Proceedings", text)
    text = re.sub(r"\.ACM,", ". ACM,", text)
    text = re.sub(r"aspartitioned", "as partitioned", text)
    text = re.sub(r"realtime", "real time", text)
    text = re.sub(r"𝑚 3\.", "𝑚 3.", text)
    return text


def merge_heading_continuation(lines: list[str]) -> list[str]:
    """Join broken headings like '4.2 Extending ...' + 'atomic global order'."""
    out = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if re.match(r"^4\.2\s+Extending Skeen", s) and nxt.lower().startswith("atomic global order"):
                rest = nxt.replace("atomic global order", "", 1).strip()
                out.append(s + " " + "atomic global order" + (" " + rest if rest else ""))
                i += 2
                continue
        out.append(lines[i])
        i += 1
    return out


def main():
    path_in = sys.argv[1] if len(sys.argv) > 1 else "paper.md"
    path_out = sys.argv[2] if len(sys.argv) > 2 else "paper.md"

    with open(path_in, "r", encoding="utf-8") as f:
        raw = f.read()

    text = fix_hyphenation(raw)
    lines = [ln.rstrip() for ln in text.split("\n")]
    lines = merge_heading_continuation(lines)

    filtered = []
    for line in lines:
        if is_noise(line):
            continue
        filtered.append(line)
    lines = filtered

    main_re = re.compile(r"^([1-6])\s+([A-Z][A-Z0-9 \-',]+)$")
    sub_re = re.compile(r"^(\d+)\.(\d+)\s+(.+)$")

    out: list[str] = []
    buf: list[str] = []

    def flush():
        nonlocal buf
        if not buf:
            return
        para = " ".join(buf)
        para = re.sub(r"\s+", " ", para).strip()
        para = fix_spaces(para)
        if para:
            out.append(para)
            out.append("")
        buf = []

    i = 0
    title_lines: list[str] = []
    while i < len(lines):
        s = lines[i].strip()
        if s == "ABSTRACT":
            break
        if s:
            title_lines.append(s)
        i += 1

    if title_lines:
        if (
            len(title_lines) >= 2
            and "Strengthening" in title_lines[0]
            and "Partitioned" in title_lines[1]
        ):
            out.append("# " + title_lines[0] + " " + title_lines[1])
            rest = title_lines[2:]
        else:
            out.append("# " + title_lines[0])
            rest = title_lines[1:]
        out.append("")
        if rest:
            out.append("*" + " · ".join(rest) + "*")
            out.append("")
        out.append("---")
        out.append("")

    if i < len(lines) and lines[i].strip() == "ABSTRACT":
        out.append("## Abstract")
        out.append("")
        i += 1
        abs_lines = []
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("ACM Reference Format:"):
                break
            if main_re.match(s) and s.startswith("1 INTRODUCTION"):
                break
            if s:
                abs_lines.append(s)
            i += 1
        abstract = " ".join(abs_lines)
        abstract = re.sub(r"\s+", " ", abstract).strip()
        out.append(abstract)
        out.append("")

    if i < len(lines) and lines[i].strip().startswith("ACM Reference Format:"):
        out.append("### ACM reference")
        out.append("")
        acm = [lines[i].strip()]
        i += 1
        while i < len(lines):
            t = lines[i].strip()
            if not t:
                i += 1
                break
            if main_re.match(t) and t.startswith("1 INTRODUCTION"):
                break
            acm.append(t)
            i += 1
        acm_text = " ".join(acm)
        acm_text = fix_spaces(re.sub(r"\s+", " ", acm_text))
        out.append(acm_text)
        out.append("")

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        if s == "REFERENCES":
            flush()
            out.append("## References")
            out.append("")
            i += 1
            ref_mode = True
            while i < len(lines):
                t = lines[i].strip()
                if not t:
                    i += 1
                    continue
                if re.match(r"^\[\d+\]", t):
                    ref = [t]
                    i += 1
                    while i < len(lines):
                        u = lines[i].strip()
                        if not u:
                            i += 1
                            break
                        if re.match(r"^\[\d+\]", u):
                            break
                        ref.append(u)
                        i += 1
                    out.append("- " + " ".join(ref))
                else:
                    i += 1
            break

        if s == "ACKNOWLEDGMENTS":
            flush()
            out.append("## Acknowledgments")
            out.append("")
            i += 1
            ack = []
            while i < len(lines):
                t = lines[i].strip()
                if not t:
                    i += 1
                    break
                if t == "REFERENCES":
                    break
                ack.append(t)
                i += 1
            out.append(" ".join(ack))
            out.append("")
            continue

        mm = main_re.match(s)
        if mm and s[0] in "123456" and len(s) < 100:
            flush()
            title = mm.group(2).strip()
            title_nice = title.title()
            title_nice = title_nice.replace("Smr", "SMR").replace("Ip ", "IP ")
            out.append(f"## {mm.group(1)}. {title_nice}")
            out.append("")
            i += 1
            continue

        ms = sub_re.match(s)
        if ms:
            flush()
            out.append(f"### {ms.group(1)}.{ms.group(2)} {ms.group(3)}")
            out.append("")
            i += 1
            continue

        if s.startswith("Figure ") and ":" in s[:50]:
            flush()
            cap = s
            i += 1
            while i < len(lines) and lines[i].strip() and not sub_re.match(lines[i].strip()) and not main_re.match(lines[i].strip()):
                nxt = lines[i].strip()
                if nxt.startswith("Figure ") or main_re.match(nxt) or sub_re.match(nxt):
                    break
                if re.match(r"^partition |^client |^atomic multicast events", nxt, re.I):
                    i += 1
                    continue
                cap += " " + nxt
                i += 1
            out.append(f"*{cap.strip()}*")
            out.append("")
            continue

        if "Figure 1:" in s or "Figure 2:" in s or "Figure 3:" in s:
            flush()
            out.append(f"*{s}*")
            out.append("")
            i += 1
            continue

        buf.append(s)
        i += 1

    flush()

    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result).strip() + "\n"

    with open(path_out, "w", encoding="utf-8") as f:
        f.write(result)
    print("Wrote", path_out, len(result), "chars")


if __name__ == "__main__":
    main()
