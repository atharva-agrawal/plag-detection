from elasticsearch import Elasticsearch, helpers
import os

es = Elasticsearch("https://localhost:9200",
    basic_auth=("elastic", "Rao6dDlctv-stCEmzTQY"),
    ca_certs="/Users/atharvaagrawal/Documents/MSc Project/plag-ai/elasticsearch-9.0.4/config/certs/http_ca.crt"
    )
index_name = "source_documents"

# Delete index if exists
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

es.indices.create(index=index_name, mappings={
    "properties": {
        "text": {"type": "text"},
        "id": {"type": "keyword"}
    }
})

actions = []
for fname in os.listdir("source-docs"):
    with open(f"source-docs/{fname}", "r") as f:
        text = f.read()
        actions.append({
            "_index": index_name,
            "_source": {
                "doc_id": fname,
                "text": text
            }
        })

helpers.bulk(es, actions)
print(f"Indexed {len(actions)} documents.")
