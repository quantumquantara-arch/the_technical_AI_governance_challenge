import pandas as pd

df = pd.read_csv("test_results.csv")
print("cols:", sorted(df.columns))
for c in ["interpreter.name","interpreter.version","verdict.severity","verdict.score"]:
    print(c, "OK" if c in df.columns else "MISSING")