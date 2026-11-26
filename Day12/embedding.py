from openai import OpenAI

client = OpenAI(
    api_key= "ollama",
    base_url= "http://localhost:11434/v1"
)

MODEL = "nomic-embed-text"

def create_embedding(text):
    response = client.embeddings.create(
        model=MODEL,
        input=text
    ) 

    return response.data[0].embedding

def embed_chunks(chunks):

    embedded_chunks = []

    for chunk in chunks:
        embed_chunk = create_embedding(chunk["chunk_text"])
        
        embedded_chunks.append({
            "chunk_text" : chunk["chunk_text"],
            "source":chunk["source"],
            "chunk_id":chunk["chunk_id"],
            "embed_chunk" : embed_chunk
            })

    return embedded_chunks


