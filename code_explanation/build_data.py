import os
import json
import glob
import re

# Root FinAgent directory
FINAGENT_DIR = "/Users/narendramishra/GEN AI /code_explanation/FinAgent"

def read_file(rel_path):
    full_path = os.path.join(FINAGENT_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

print("Building data generator for FinAgent documentation...")
