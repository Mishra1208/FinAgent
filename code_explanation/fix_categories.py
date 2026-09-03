import json

with open("/Users/narendramishra/GEN AI /code_explanation/src/data/projectData.js", "r", encoding="utf-8") as f:
    content = f.read()

# Parse the JSON from the JS file
prefix = "// MASTER FINAGENT CODE EXPLANATION DATASET\nexport const PROJECT_MODULES = "
json_str = content.replace(prefix, "").rstrip(";\n")
modules = json.loads(json_str)

for m in modules:
    if m["id"] == "grounding-masterclass":
        m["category"] = "10. Factual Grounding & 96.4% Benchmark"
    elif m["id"] == "requirements-guide":
        m["category"] = "11. Python Dependencies (requirements.txt)"

with open("/Users/narendramishra/GEN AI /code_explanation/src/data/projectData.js", "w", encoding="utf-8") as f:
    f.write(f"// MASTER FINAGENT CODE EXPLANATION DATASET\nexport const PROJECT_MODULES = {json.dumps(modules, indent=2)};\n")

print("Updated categories in projectData.js: Category 10 and Category 11 are cleanly separated!")
