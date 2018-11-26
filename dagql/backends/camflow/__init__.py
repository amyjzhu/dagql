import io
import json
import logging
import subprocess
from collections import defaultdict, deque

from dagql.backend import Backend, Node, TraversalOrder


NAMESPACE = b'dagql'
START_DIRECTIVE = NAMESPACE + b': #start'
NAMESPACE_PREFIX = NAMESPACE + b': '


class CamFlowNode(Node):
    """DAGQL node representation"""
    def __init__(self, attrdict: dict):
        self.attrs = attrdict

    def __getitem__(self, attr: str):
        return self.attrs[attr]


class CamFlowBackend(Backend):
    """
    DAGQL backend for querying CamFlow provenance graphs.

    Requires the provenance2json CamQuery hook to be loaded.
    """
    def __init__(self, msgbuf=None):
        if msgbuf is None:
            result = subprocess.run(['dmesg', '-t'], stderr=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE)
            msgbuf = io.BytesIO(result.stdout)

        self._reset_graph()

        warned = False
        for line in msgbuf:
            if line.startswith(START_DIRECTIVE):
                self._reset_graph()
            elif line.startswith(NAMESPACE_PREFIX):
                (from_, edge, to) = json.loads(line[len(NAMESPACE_PREFIX):])
                if from_ is None or to is None:
                    if not warned:
                        logging.warning('One or more nodes were dropped due to '
                                        'a serialization error. Check dmesg.')
                        warned = True
                    continue
                from_id = from_['id']
                to_id = to['id']
                if not from_id in self.nodes:
                    self.nodes[from_id] = from_
                if not to_id in self.nodes:
                    self.nodes[to_id] = to
                self.nodes[to_id]['_has_incoming'] = True
                self.outgoing[from_id].append((edge, to_id))
        # nodes to begin traversal from
        self.starts = [n for n in self.nodes.values() if not n.get('_has_incoming')]

    def _reset_graph(self):
        self.nodes = dict()
        self.outgoing = defaultdict(list)
        self.starts = set()

    def walk(self, traversal: TraversalOrder):
        if traversal == TraversalOrder.DFS:
            return self._dfs_walk()
        if traversal == TraversalOrder.BFS:
            return self._bfs_walk()
        raise ValueError('unknown TraversalOrder %s' % traversal)

    def _dfs_walk(self):
        stack = list(self.starts)
        while stack:
            node = stack.pop()
            print('Node %s' % node['id'])
            outgoing_edges = self.outgoing[node['id']]
            for (_edge, to_id) in outgoing_edges:
                # this means we can visit nodes multiple times if there are
                # multiple edges going into a node...
                print('Pushing %s' % to_id)
                stack.append(self.nodes[to_id])
            yield CamFlowNode(node)

    def _bfs_walk(self):
        queue = deque(self.starts)
        while queue:
            node = queue.pop()
            outgoing_edges = self.outgoing[node['id']]
            for (_edge, to_id) in outgoing_edges:
                queue.appendleft(self.nodes[to_id])
            yield CamFlowNode(node)
