import pytest

from dagql.backend import Backend, Node


@pytest.mark.xfail(strict=True)
def test_no_instantiate_node():
    _ = Node()

@pytest.mark.xfail(strict=True)
def test_no_instantiate_backend():
    _ = Backend()
