import os

from dagql.backend import Backend, Node, Edge, TraversalOrder


class FileSystemNode(Node):
    def __init__(self, dirpath: str, basename: str, isdir: bool):
        self.dirpath = dirpath
        self.basename = basename
        self.isdir = isdir

    def __getitem__(self, attr: str):
        if attr == 'type':
            return ('directory' if self.isdir else 'file')
        if attr == 'dirname':
            return self.dirpath
        if attr == 'basename':
            return self.basename
        if attr == 'contents' and not self.isdir:
            # example of lazily computed attribute
            # note this does not work for non-UTF-8 files, but DAGQL does not
            # have a binary type
            return open(os.path.join(self.dirpath, self.basename), 'r').read()
        raise KeyError(attr)


class FileSystemEdge(Edge):
    def __init__(self):
        pass

    def __getitem__(self, attr: str):
        raise KeyError(attr) # no interesting attributes


class FileSystemBackend(Backend):
    """
    DAGQL backend for querying files and directories.

    DFS is implemented as a post-order traversal.  This means children will be
    listed before parents.
    """
    def __init__(self, rootdir: str):
        self.rootdir = rootdir

    def walk_nodes(self, traversal: TraversalOrder):
        if traversal not in {TraversalOrder.DFS, TraversalOrder.BFS}:
            raise ValueError('unknown TraversalOrder %s' % traversal)

        topdown = (traversal == TraversalOrder.BFS)
        for (dirpath, dirnames, filenames) in os.walk(self.rootdir,
                                                      topdown=topdown):
            yield from (FileSystemNode(dirpath, d, True) for d in dirnames)
            yield from (FileSystemNode(dirpath, f, False) for f in filenames)

    def walk_edges(self, traversal: TraversalOrder):
        if traversal not in {TraversalOrder.DFS, TraversalOrder.BFS}:
            raise ValueError('unknown TraversalOrder %s' % traversal)

        topdown = (traversal == TraversalOrder.BFS)
        for (dirpath, dirnames, filenames) in os.walk(self.rootdir,
                                                      topdown=topdown):
            parent = FileSystemNode(os.path.dirname(dirpath),
                                    os.path.basename(dirpath), True)
            yield from ((FileSystemEdge(), parent,
                         FileSystemNode(dirpath, d, True)) for d in dirnames)
            yield from ((FileSystemEdge(), parent,
                         FileSystemNode(dirpath, f, False)) for f in filenames)
