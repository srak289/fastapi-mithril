from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def main():
    return {"response": "pong"}

@app.get("/api/ping")
def ping():
    return {"pong"}

