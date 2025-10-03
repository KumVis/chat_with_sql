import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="SQL Query API with Groq")

# Database connection (SQLite for now)
db = SQLDatabase.from_uri("sqlite:///sample.db")

# Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-20b",
    temperature=0
)

# SQL Chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Define request body schema
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def run_query(req: QueryRequest):
    try:
        # Step 1: Generate SQL query from LLM
        sql_prompt = f"Translate the following question into a valid SQLite SQL query (no explanations, no markdown, just SQL):\n{req.question}"
        sql_query = llm.predict(sql_prompt).strip()

        # Step 2: Remove markdown if LLM still adds it
        if sql_query.startswith("```"):
            sql_query = sql_query.split("```")[1]  # take content inside fences
        sql_query = sql_query.replace("sql", "").strip()

        # Step 3: Run SQL against DB
        sql_result = db.run(sql_query)

        # Step 4: Wrap everything into final response
        return {
            "question": req.question,
            "sql_query": sql_query,
            "sql_result": sql_result,
            "final_answer": f"Result: {sql_result}"
        }

    except Exception as e:
        return {"error": str(e)}



# Health check route
@app.get("/")
def home():
    return {"message": "SQL Query API is running!"}
