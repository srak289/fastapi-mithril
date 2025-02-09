from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/nodes")
def nodes():
    return dict(elements=[
        dict(data=dict(id="a")),
        dict(data=dict(id="b")),
        dict(data=dict(id="c")),
        dict(data=dict(id="d")),
        dict(data=dict(id="e")),
        dict(data=dict(id="ab", source="a", target="b")),
        dict(data=dict(id="ac", source="a", target="c")),
        dict(data=dict(id="bd", source="b", target="d")),
        dict(data=dict(id="ce", source="c", target="e")),
    ])

@app.get("/api/ping")
def ping():
    return {"pong"}

@app.get("/api")
def main():
    return {"hello"}

