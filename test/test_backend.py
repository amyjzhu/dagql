import os

import pytest

from dagql.backend import Backend, Node, TraversalOrder
from dagql.backends.camflow import CamFlowBackend


@pytest.mark.xfail(strict=True)
def test_no_instantiate_node():
    _ = Node()

@pytest.mark.xfail(strict=True)
def test_no_instantiate_backend():
    _ = Backend()

# FIXME: This test sometimes runs forever since the graph sometimes has cycles.
#        Need to look into this.
# @pytest.mark.skipif('camflow' not in os.uname().release, reason='requires camflow')
@pytest.mark.skip(reason='')
def test_smoke():
    """Simple smoke test to make sure nothing blows up."""
    cf = CamFlowBackend()
    for _ in cf.walk(TraversalOrder.DFS):
        pass

BASIC_MSGBUF = os.path.join(os.path.dirname(__file__), "inputs", "basic.txt")
def test_basic():
    cf = CamFlowBackend(open(BASIC_MSGBUF, 'rb'))
    it = cf.walk(TraversalOrder.DFS)

    node = next(it)
    assert node['id'] == 218451
    assert node['type'] == 'path'
    assert node['path'] == '/usr/bin/grep'

    node = next(it)
    assert node['id'] == 218450 # child of 218451
    assert node['type'] == 'file'
    assert node['inode'] == 793325

    node = next(it)
    assert node['id'] == 359384
    assert node['type'] == 'file'

    node = next(it)
    assert node['id'] == 359389 # child of 349384
    assert node['type'] == 'file'

    node = next(it)
    assert node['id'] == 31996 # child of 349384
    assert node['type'] == 'task'

    node = next(it)
    assert node['id'] == 359380
    assert node['type'] == 'path'
    assert node['path'] == '/525/cgroup'

    node = next(it)
    assert node['id'] == 359379 # child of 359380
    assert node['type'] == 'file'
    assert node['inode'] == 144143
    assert node['mode'] == 33060

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass


def test_basic_bfs():
    cf = CamFlowBackend(open(BASIC_MSGBUF, 'rb'))
    it = cf.walk(TraversalOrder.BFS)

    node = next(it)
    assert node['id'] == 218451

    node = next(it)
    assert node['id'] == 359384

    node = next(it)
    assert node['id'] == 359380

    node = next(it)
    assert node['id'] == 218450 # child of 218451

    node = next(it)
    assert node['id'] == 31996 # child of 349384

    node = next(it)
    assert node['id'] == 359389 # child of 349384

    node = next(it)
    assert node['id'] == 359379 # child of 359380

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass

HAS_NULL_MSGBUF = os.path.join(os.path.dirname(__file__), "inputs", "has_null.txt")
def test_drop_nulls():
    cf = CamFlowBackend(open(HAS_NULL_MSGBUF, 'rb'))
    assert len(list(cf.walk(TraversalOrder.DFS))) == 2

UNICODE_MSGBUF = os.path.join(os.path.dirname(__file__), "inputs", "unicode.txt")
def test_unicode():
    cf = CamFlowBackend(open(UNICODE_MSGBUF, 'rb'))
    it = cf.walk(TraversalOrder.BFS)

    node = next(it)
    assert node['id'] == 218451
    assert node['path'] == '/usr/bin/🐎'

    node = next(it)
    assert node['id'] == 218450

    try:
        next(it)
        assert 0, 'iterator should have no more elements'
    except StopIteration:
        pass

EMPTY_MSGBUF = os.path.join(os.path.dirname(__file__), "inputs", "empty.txt")
def test_empty():
    cf = CamFlowBackend(open(EMPTY_MSGBUF, 'rb'))
    assert [] == list(cf.walk(TraversalOrder.DFS))
