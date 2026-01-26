import json
import pandas as pd

df = pd.read_csv("test_results.csv")
out = "trace_output.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for _, r in df.iterrows():
        obj = {}
        for k, v in r.to_dict().items():
            if isinstance(v, float) and (v != v):
                obj[k] = None
            else:
                obj[k] = v
        f.write(json.dumps(obj, ensure_ascii=True, sort_keys=True) + "\n")
print("wrote", out)
