import json
from pathlib import Path

subagent_log = Path(r"C:\Users\USER\.gemini\antigravity\brain\a0fc8fb5-3d0d-4d84-87a9-8cf05e718c17\.system_generated\logs\transcript.jsonl")

with open(subagent_log, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if obj.get("step_index") in range(235, 245):
            print(f"STEP {obj.get('step_index')}: {obj.get('type')}")
            if "tool_calls" in obj:
                for tc in obj["tool_calls"]:
                    print("   TOOL:", tc["name"], str(tc.get("args", {}))[:300])
            if "content" in obj and "Command output" in obj["content"]:
                print("   OUTPUT:", obj["content"][:300])
