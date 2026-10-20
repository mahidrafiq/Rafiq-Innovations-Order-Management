"""Tests for the order-management logic in ``main.py``.

Run with:

    python -m pytest -q
"""
import builtins

import pytest

import main as app


def test_find_product_is_case_and_space_insensitive():
    product = app.find_product("  WALNUT CRACKER ")
    assert product is not None
    assert product.name == "Walnut Cracker"
    assert product.price == 50000.0


def test_find_product_returns_none_for_unknown_item():
    assert app.find_product("Nonexistent Item") is None


def test_save_order_computes_total_and_persists(tmp_path):
    db = app.OrderDatabase(tmp_path / "orders.db")
    order_id, total, created_at = db.save_order(
        "Ahmad Khan", app.PRODUCTS["walnut cracker"], 2
    )
    assert order_id.startswith("RI-")
    assert len(order_id) == 11
    assert total == 100000.0

    rows = db.recent_orders()
    assert len(rows) == 1
    assert rows[0][0] == order_id


def test_ask_positive_integer_reprompts_until_valid(monkeypatch):
    answers = iter(["abc", "0", "-3", "5"])
    monkeypatch.setattr(builtins, "input", lambda *_: next(answers))
    assert app.ask_positive_integer("Quantity: ") == 5


def test_order_ids_are_unique(tmp_path):
    db = app.OrderDatabase(tmp_path / "orders.db")
    product = app.PRODUCTS["multipurpose axe"]
    ids = {db.save_order("Customer", product, 1)[0] for _ in range(50)}
    assert len(ids) == 50
