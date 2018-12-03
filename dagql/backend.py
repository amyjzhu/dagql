from enum import Enum
from typing import Iterator, Tuple


class TraversalOrder(Enum):
    DFS = 0
    BFS = 1


class Node:
    """
    Opaque representation of a node.

    The implementation details of this node may vary from backend to backend.
    In general, you are not allowed to use nodes received as output from one
    backend as input to another.
    """
    def __init__(self):
        raise NotImplementedError

    def __getitem__(self, attr: str):
        """
        Get an attribute of a node.  The attribute may or may not be computed
        on request (such details depend on the implementation, even on a
        per-attribute basis).

        Raises:
            KeyError: If the node does not contain the given attribute.

        Returns:
            The requested attribute.
        """
        raise NotImplementedError


class Edge:
    """
    Opaque representation of an edge.

    The implementation details of this edge may vary from backend to backend.
    In general, you are not allowed to use edges received as output from one
    backend as input to another.
    """
    def __init__(self):
        raise NotImplementedError

    def __getitem__(self, attr: str):
        """
        Get an attribute of an edge.  The attribute may or may not be computed
        on request (such details depend on the implementation, even on a
        per-attribute basis).

        Raises:
            KeyError: If the edge does not contain the given attribute.

        Returns:
            The requested attribute.
        """
        raise NotImplementedError


class Backend:
    """
    Interface hiding away implementation details of querying a domain-specific
    directed acyclic graph.
    """
    def __init__(self):
        raise NotImplementedError

    def walk_nodes(self, traversal: TraversalOrder) -> Iterator[Node]:
        """
        Iterate over the nodes in a directed acyclic graph by walking the graph
        via the specified traversal order.

        Args:
            traversal: Order in which nodes are generated.

        Returns:
            An iterator which yields nodes from the graph one by one.
        """
        raise NotImplementedError

    def walk_edges(self, traversal: TraversalOrder) -> Iterator[Tuple[Edge, Node, Node]]:
        """
        Iterate over the edges in a directed acyclic graph by walking the graph
        via the specified traversal order.

        Args:
            traversal: Order in which nodes are generated.

        Returns:
            An iterator which yields nodes from the graph one by one.
        """
        raise NotImplementedError
