import os

import json
import sqlite3
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI


DATABASE = "memory.db"
load_dotenv()


# embedding_client = OpenAI(
#     base_url=os.getenv("BASE_URL"),
#     api_key=os.getenv("API_KEY_E")
# )
embedding_client = OpenAI(
   base_url=os.getenv("BASE_URL"),
   api_key=os.getenv("NVDIA_API_KEY")
)

def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            assistant_message TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_message TEXT,
                embedding TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    connection.commit()
    connection.close()


def create_embedding(text, input_type="query"):
    # response = embedding_client.embeddings.create(
    #     model=os.getenv("E_MODEL"),
    #     input=text
    # )
    response = embedding_client.embeddings.create(
    input=text,
    model=os.getenv("E_MODEL"),
    encoding_format="float",
    extra_body={
        "input_type": input_type
    }    
)
    
    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )


def save_memory(user_message, assistant_message):
    text = user_message + "\n" + assistant_message

    embedding = create_embedding(text)
    

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories
        (
            user_message,
            assistant_message,
            embedding
        )
        VALUES (?, ?, ?)
        """,
        (
            user_message,
            assistant_message,
            json.dumps(embedding)
        )
    )

    connection.commit()
    connection.close()


def save_semantic_memory(fact):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Check exact duplicate
    cursor.execute(
        """
        SELECT id
        FROM facts
        WHERE LOWER(TRIM(fact_message)) = LOWER(TRIM(?))
        """,
        (fact,)
    )

    existing = cursor.fetchone()

    if existing:
        connection.close()
        print("Fact already exists. Skipping insertion.")
        return False

    # Generate embedding only for new facts
    embedding = create_embedding(
        fact,
        input_type="passage"
    )

    cursor.execute(
        """
        INSERT INTO facts (fact_message, embedding)
        VALUES (?, ?)
        """,
        (fact, json.dumps(embedding))
    )

    connection.commit()
    connection.close()

    print("New fact saved successfully.")
    return True



def search_semantic_memories(
    query,
    top_k=3,
    threshold=0.10
):
    query_embedding = create_embedding(query)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            fact_message,
            embedding,
            created_at
        FROM facts
    """)

    rows = cursor.fetchall()

    connection.close()

    results = []

    for (
        fact_message,
        embedding_json,
        created_at
    ) in rows:

        memory_embedding = json.loads(
            embedding_json
        )

        score = cosine_similarity(
            query_embedding,
            memory_embedding
        )
        
        if score >= threshold:
            results.append({
                "user_message": fact_message,
                "created_at": created_at,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    print(results)

    return results[:top_k]

