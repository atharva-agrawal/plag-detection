import pandas as pd
import os

csv_file = "/Users/atharvaagrawal/Documents/MSc Project/plag-ai/data/generated/responses_llama3.1:8b.csv"  # change to mistral/gemma as needed

df = pd.read_csv(csv_file)
os.makedirs("source-docs", exist_ok=True)
os.makedirs("suspicious-docs", exist_ok=True)

with open("pairs.txt", "w") as pf:
    for i, row in df.iterrows():
        sid = f"{i+1:05}"
        src_path = f"source000{sid}.txt"
        susp_path = f"suspicious000{sid}.txt"

        # Simulated source = prompt
        with open(f"source-docs/{src_path}", "w") as f:
            f.write(row['prompt_text'])

        # Suspicious = model response
        with open(f"suspicious-docs/{susp_path}", "w") as f:
            f.write(row['response'])

        pf.write(f"{susp_path} {src_path}\n")
