import os

def ingest_documents(directory="docs"):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]