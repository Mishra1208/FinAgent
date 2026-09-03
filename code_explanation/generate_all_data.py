import os
import json
import re

BASE_DIR = "/Users/narendramishra/GEN AI /code_explanation/FinAgent"

def read_finagent_file(rel_path):
    p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def split_python_into_sections(code_str, filename):
    lines = code_str.split("\n")
    sections = []
    
    # Heuristically split Python code by imports, class definitions, function definitions, or major blocks
    boundaries = [0]
    for i, line in enumerate(lines):
        if i == 0:
            continue
        stripped = line.strip()
        # Top-level class or function definition, or major comments
        if (line.startswith("class ") or 
            line.startswith("def ") or 
            line.startswith("@tool") or
            line.startswith("@classmethod") or
            line.startswith("# ----") or
            (stripped.startswith("class ") and not line.startswith(" ")) or
            (stripped.startswith("def ") and not line.startswith("    "))):
            if i not in boundaries and (i - boundaries[-1]) >= 4:
                boundaries.append(i)
        elif line.startswith("# Singleton") or line.startswith("# Ingest") or line.startswith("# Query"):
            if i not in boundaries and (i - boundaries[-1]) >= 4:
                boundaries.append(i)

    boundaries.append(len(lines))
    
    # Remove duplicates and sort
    boundaries = sorted(list(set(boundaries)))
    
    for idx in range(len(boundaries) - 1):
        s_line = boundaries[idx]
        e_line = boundaries[idx + 1]
        chunk_lines = lines[s_line:e_line]
        chunk_code = "\n".join(chunk_lines).strip()
        if not chunk_code:
            continue
        
        # Determine chunk title
        first_line = chunk_lines[0].strip()
        for cl in chunk_lines:
            if cl.strip().startswith("class "):
                first_line = cl.strip().split(":")[0]
                break
            elif cl.strip().startswith("def "):
                first_line = cl.strip().split(":")[0]
                break
            elif cl.strip().startswith("import ") or cl.strip().startswith("from "):
                first_line = "Imports & Dependencies"
                break
            elif cl.strip().startswith("#"):
                first_line = cl.strip().replace("#", "").strip()
                break

        sections.append({
            "sectionId": f"sec-{idx+1}",
            "startLine": s_line + 1,
            "endLine": e_line,
            "title": first_line[:60],
            "code": chunk_code,
            "simpleExplanation": "",
            "whyWrittenThisWay": "",
            "interviewTips": ""
        })
    
    return sections

print("Data generator ready.")
