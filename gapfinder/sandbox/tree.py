"""Checkpoint tree: image ids plus metadata (layer, applied changes, parent).

Key nodes get tags such as `gf/ruskey/built` so the 180-day cleanup of
untagged images never touches them. The tree can be rebuilt from the event
log alone (`CheckpointTree.replay`), which is what replay mode relies on.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable

from gapfinder.ledger.schemas import Layer

# Depth order: a knob of layer L must fork from a checkpoint no deeper than this.
LAYER_DEPTH = {"source": 0, "build": 0, "built": 1, "dataset": 1, "loaded": 2, "config": 2, "workload": 2, "environment": 2}
STAGE_FOR_LAYER = {
    Layer.build.value: "source",  # build flags need a rebuild from source
    Layer.dataset.value: "built",  # dataset knobs reload from the built image
    Layer.config.value: "loaded",
    Layer.workload.value: "loaded",
    Layer.environment.value: "loaded",
}


@dataclass
class Node:
    id: str
    parent: str | None
    stage: str  # source | built | loaded | branch
    changes: dict[str, str] = field(default_factory=dict)
    tag: str | None = None
    command: str | None = None
    cost_usd: float = 0.0
    elapsed_s: float = 0.0


class CheckpointTree:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.stage_index: dict[tuple[str, tuple], str] = {}  # (stage, frozen build changes) -> id

    def add(self, node: Node) -> Node:
        """Sandbox checkpoint IDs are content-addressed: a run that changes nothing on disk returns
        its parent's ID. Such a no-op node isn't stored again (it would be its own parent);
        the existing node just also serves as this stage's checkpoint."""
        if node.parent == node.id or (node.id in self.nodes and node.stage != "branch"
                                      and self.nodes[node.id].stage != node.stage):
            existing = self.nodes.get(node.id)
            if existing is not None:
                if node.stage in ("source", "built", "loaded"):
                    key = (node.stage, _freeze({**self._lineage_changes(node.id, build_only=True), **node.changes}))
                    self.stage_index[key] = node.id
                return existing
            node.parent = None
        self.nodes[node.id] = node
        if node.stage in ("source", "built", "loaded"):
            self.stage_index[(node.stage, _freeze(self._lineage_changes(node.id, build_only=True)))] = node.id
        return node

    def _lineage_changes(self, nid: str, build_only: bool = False) -> dict[str, str]:
        chain, cur, seen = [], self.nodes.get(nid), set()
        while cur is not None and cur.id not in seen:  # never loop, even on a malformed tree
            seen.add(cur.id)
            chain.append(cur)
            cur = self.nodes.get(cur.parent) if cur.parent else None
        out: dict[str, str] = {}
        for n in reversed(chain):
            if build_only and n.stage not in ("source", "built", "loaded"):
                continue
            out.update(n.changes)
        return out

    def lineage_changes(self, nid: str) -> dict[str, str]:
        return self._lineage_changes(nid)

    def find_stage(self, stage: str, build_changes: dict[str, str] | None = None) -> str | None:
        return self.stage_index.get((stage, _freeze(build_changes or {})))

    def children(self, nid: str) -> list[Node]:
        return [n for n in self.nodes.values() if n.parent == nid]

    def to_dict(self) -> dict:
        return {nid: asdict(n) for nid, n in sorted(self.nodes.items())}

    @classmethod
    def replay(cls, events: Iterable[dict]) -> "CheckpointTree":
        tree = cls()
        for ev in events:
            if ev["type"] == "checkpoint":
                tree.add(Node(**ev["node"]))
        return tree


def depth_plan(layer: str) -> str:
    """The deepest stage still valid for a knob of this layer."""
    return STAGE_FOR_LAYER.get(layer, "loaded")


def _freeze(d: dict) -> tuple:
    return tuple(sorted(d.items()))
