import io
import json
import logging
import subprocess
from collections import defaultdict, deque

from dagql.backend import Backend, Node, Edge, TraversalOrder


NAMESPACE = b'dagql'
START_DIRECTIVE = NAMESPACE + b': #start'
NAMESPACE_PREFIX = NAMESPACE + b': '


class CamFlowNode(Node):
    """DAGQL node representation"""
    def __init__(self, attrdict: dict):
        self.attrs = attrdict

    def __getitem__(self, attr: str):
        return self.attrs[attr.lower()]


class CamFlowEdge(Edge):
    """DAGQL edge representation"""
    def __init__(self, attrdict: dict):
        self.attrs = attrdict

    def __getitem__(self, attr: str):
        return self.attrs[attr.lower()]


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
                self.nodes[to_id]['_Has_incoming'] = True
                self.outgoing[from_id].append((edge, to_id))
        # nodes to begin traversal from
        self.starts = [n for n in self.nodes.values() if not n.get('_Has_incoming')]

    def _reset_graph(self):
        self.nodes = dict()
        self.outgoing = defaultdict(list)
        self.starts = set()

    def walk_nodes(self, traversal: TraversalOrder):
        if traversal == TraversalOrder.DFS:
            stack = list(self.starts)
            return self._nodewalk(stack, stack.pop, stack.append)
        if traversal == TraversalOrder.BFS:
            queue = deque(self.starts)
            return self._nodewalk(queue, queue.pop, queue.appendleft)
        raise ValueError('unknown TraversalOrder %s' % traversal)

    def walk_edges(self, traversal: TraversalOrder):
        if traversal == TraversalOrder.DFS:
            stack = []
            for node in self.starts:
                for (edge, to_id) in self.outgoing[node['id']]:
                    stack.append((edge, node, self.nodes[to_id]))
            stack.reverse() # makes order slightly nicer if there was "natural"
                            # order in the first place
            return self._edgewalk(stack, stack.pop,
                                  # reversed makes order slightly nicer
                                  lambda ns: stack.extend(reversed(ns)))
        if traversal == TraversalOrder.BFS:
            queue = deque()
            for node in self.starts:
                for (edge, to_id) in self.outgoing[node['id']]:
                    queue.append((edge, node, self.nodes[to_id]))
            return self._edgewalk(queue, queue.popleft, queue.extend)
        raise ValueError('unknown TraversalOrder %s' % traversal)

    def _nodewalk(self, container, pop, push):
        while container:
            node = pop()
            outgoing_edges = self.outgoing[node['id']]
            for (_edge, to_id) in outgoing_edges:
                # this means we can visit nodes multiple times if there are
                # multiple edges going into a node...
                push(self.nodes[to_id])
            yield CamFlowNode(node)

    def _edgewalk(self, container, pop, extend):
        while container:
            (edge, from_node, to_node) = pop()
            outgoing_edges = self.outgoing[to_node['id']]
            extend([(to_edge, to_node, self.nodes[to_to_id])
                    for (to_edge, to_to_id) in outgoing_edges])
            yield (CamFlowEdge(edge), CamFlowNode(from_node),
                   CamFlowNode(to_node))
