import os

import pytest

from main import VECTOR_DIM


def test_vector_dimension_is_positive():
    assert VECTOR_DIM > 0


def test_token_is_not_hardcoded():
    source = open("main.py", encoding="utf-8").read()
    assert "MILVUS_TOKEN=" not in source
    assert "sk-" not in source


def test_missing_uri_is_detectable(monkeypatch):
    monkeypatch.delenv("MILVUS_URI", raising=False)
    with pytest.raises(KeyError):
        os.environ["MILVUS_URI"]
