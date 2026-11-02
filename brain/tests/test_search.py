from app.menu.search import search_products


def test_search_cheese() -> None:
    products = search_products("cheese")

    assert products
    assert products[0].name.lower() == "cheeseburger"


def test_search_x_burguer() -> None:
    products = search_products("x burguer")

    assert products
    assert products[0].name.lower() == "x-burger"


def test_search_suco() -> None:
    products = search_products("suco")

    assert products
    assert products[0].name.lower() == "suco de laranja"


def test_search_without_product() -> None:
    products = search_products("pizza sem queijo")

    assert products == []
