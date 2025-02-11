import string
import random
import yaml

from dataclasses import dataclass, field
from fastapi import FastAPI

app = FastAPI()

@dataclass
class Node:
    id: str

    def to_dict(self):
        return dict(data=dict(id=self.id))

@dataclass
class Edge:
    source: Node
    target: Node
    id: str = None

    def __post_init__(self):
        self.id = self.source.id + "-" + self.target.id

    def to_dict(self):
        return dict(data=dict(id=self.id, source=self.source.id, target=self.target.id))

@dataclass
class Graph:
    nodes: [Node] = field(default_factory=lambda: [])
    edges: [Edge] = field(default_factory=lambda: [])

    def add_node(self, id):
        self.nodes.append(Node(id))

    def add_edge(self, s: Node, t: Node):
        if s not in self.nodes:
            raise ValueError(f"{s} not in Nodes")
        if t not in self.nodes:
            raise ValueError(f"{t} not in Nodes")
        self.edges.append(Edge(s, t))

    def to_dict(self):
        ret = dict(elements=[])
        for n in self.nodes:
            ret["elements"].append(n.to_dict())
        for e in self.edges:
            ret["elements"].append(e.to_dict())
        return ret

random_letter = lambda: random.choice(string.ascii_lowercase)

@app.get("/api/v1/nodes")
def nodes():
    graph = Graph()

    for n in range(10, random.randint(10,30)):
        while 1:
            n = "".join([random_letter() for _ in range(3)])
            if Node(n) not in graph.nodes:
                break
        graph.add_node(n)

    for e in range(10, random.randint(10,30)):
        while 1:
            s = random.choice(graph.nodes)
            t = random.choice(graph.nodes)
            if s != t:
                break
        graph.add_edge(s, t)

    return graph.to_dict()

@app.get("/api/ping")
def ping():
    return {"pong"}

@app.get("/api")
def main():
    return {"hello"}

