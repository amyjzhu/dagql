import os

from dagql.backend import Edge, TraversalOrder
from dagql.backends.filesystem import FileSystemBackend


TEST_DIR = os.path.join(os.path.dirname(__file__), "inputs", "test-fs")


def test_nodewalk_dfs():
    fs = FileSystemBackend(TEST_DIR)
    it = fs.walk_nodes(TraversalOrder.DFS)

    node = next(it)
    assert node['basename'] == 'a.txt'
    assert node['contents'] == 'quux\n'
    assert node['type'] == 'file'

    node = next(it)
    assert node['basename'] == 'a'
    assert node['type'] == 'directory'

    node = next(it)
    assert node['basename'] == 'b.txt'
    assert node['contents'] == 'foo\n'

    node = next(it)
    assert node['basename'] == 'c.txt'
    assert node['contents'] == 'bar\n'

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass


def test_nodewalk_bfs():
    fs = FileSystemBackend(TEST_DIR)
    it = fs.walk_nodes(TraversalOrder.BFS)

    node = next(it)
    assert node['basename'] == 'a'
    assert node['type'] == 'directory'

    node = next(it)
    assert node['basename'] == 'b.txt'
    assert node['contents'] == 'foo\n'

    node = next(it)
    assert node['basename'] == 'c.txt'
    assert node['contents'] == 'bar\n'

    node = next(it)
    assert node['basename'] == 'a.txt'
    assert node['contents'] == 'quux\n'

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass


def test_edgewalk_bfs():
    fs = FileSystemBackend(TEST_DIR)
    it = fs.walk_edges(TraversalOrder.BFS)

    (edge, from_, to) = next(it)
    assert isinstance(edge, Edge)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'a'

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'b.txt'

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'c.txt'

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'a'
    assert to['basename'] == 'a.txt'

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass


def test_edgewalk_dfs():
    fs = FileSystemBackend(TEST_DIR)
    it = fs.walk_edges(TraversalOrder.DFS)

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'a'
    assert to['basename'] == 'a.txt'

    (edge, from_, to) = next(it)
    assert isinstance(edge, Edge)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'a'

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'b.txt'

    (edge, from_, to) = next(it)
    assert from_['basename'] == 'test-fs'
    assert to['basename'] == 'c.txt'

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass
