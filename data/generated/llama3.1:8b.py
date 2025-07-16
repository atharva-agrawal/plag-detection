import pandas as pd
import requests
import json
import time

MODEL = "llama3.1:8b"

# Loading prompt.csv file
df = pd.read_csv("./prompts.csv")


# To store response
results = []

# Loop over each prompt and send to API
for i, row in df.iterrows():
    prompt_id = row['prompt_id']
    category = row['category']
    prompt = row['text']

    try:
        #Request to local Ollama server
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": MODEL, "prompt": prompt},
            stream=True
        )
        if response.status_code == 200:
            full_response = ""
        
        # Iterate over the streamed chunks of data
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode("utf-8"))
                full_response += data["response"]
                # Check if the response is complete (done is True)
                if data.get("done"):
                    break
        
        results.append({
            "prompt_id": prompt_id,
            "category": category,
            "prompt_text": prompt,
            "model": MODEL,
            "response": full_response
        })

        print(f"{prompt_id} done.")
        time.sleep(1)

    except Exception as e:
        print(f"Error on {prompt_id}: {e}")
        results.append({
            "prompt_id": prompt_id,
            "category": category,
            "prompt_text": prompt,
            "model": MODEL,
            "response": "ERROR"
        })

# Convert to DataFrame and save to csv
df_out = pd.DataFrame(results)
df_out.to_csv(f"responses_{MODEL}.csv", index=False)
print(f"All done. Saved to responses_{MODEL}.csv")
