from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from app.menu.models import Product

_STOP_WORDS = {
    "a",
    "as",
    "com",
    "da",
    "de",
    "do",
    "dos",
    "e",
    "gostaria",
    "me",
    "minha",
    "o",
    "os",
    "para",
    "por",
    "pra",
    "quais",
    "qual",
    "quer",
    "quero",
    "sem",
    "um",
    "uma",
    "uns",
    "umas",
    "vou",
}


def _normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def _tokenize(value: str) -> list[str]:
    normalized = _normalize_text(value)
    return [token for token in normalized.split() if token and token not in _STOP_WORDS]


def _load_products() -> list[Product]:
    menu_path = Path(__file__).with_name("menu.json")
    payload = json.loads(menu_path.read_text(encoding="utf-8"))
    return [Product.model_validate(item) for item in payload["products"]]


def search_products(text: str) -> list[Product]:
    if not text or not text.strip():
        return []

    query_tokens = _tokenize(text)
    if not query_tokens:
        return []

    query_text = " ".join(query_tokens)
    ranked_products: list[tuple[int, Product]] = []

    for product in _load_products():
        product_tokens = _tokenize(product.name)
        product_text = " ".join(product_tokens)
        score = 0

        if query_text == product_text:
            score += 100
        if query_text in product_text or product_text in query_text:
            score += 40

        for token in query_tokens:
            if token in product_tokens:
                score += 20
                continue

            if any(token in candidate or candidate in token for candidate in product_tokens):
                score += 12
                continue

            if any(SequenceMatcher(None, token, candidate).ratio() >= 0.75 for candidate in product_tokens):
                score += 8

        if score > 0:
            ranked_products.append((score, product))

    ranked_products.sort(key=lambda item: (-item[0], item[1].name))
    return [product for _, product in ranked_products]
