from dataclasses import dataclass
from typing import Any, Tuple

NAME_COLUMN_CLASS_PATTERN = "td[class$=Titre]"
NAME_COLUMN_HEADER_TYPE = "h4"
QUANTITY_COLUMN_CLASS_PATTERN = "p[class$=Quantite]"
PRICE_COLUMN_PATTERN = "p[class$=Prix]"


@dataclass(frozen=True)
class ProductInOrder:
    category_name: str
    product_name: str
    quantity: int
    unit_price: float
    price: float

    @classmethod
    def from_row(cls, category_name: str, row: Any):
        product_name = _get_product_name_from_row(row)
        quantity = _get_quantity_from_row(row)
        price = _get_price_from_row(row)
        unit_price = price / quantity
        return cls(
            category_name=category_name,
            product_name=product_name,
            quantity=quantity,
            price=price,
            unit_price=unit_price,
        )

    def to_tuple(self) -> Tuple[str, str, int, float, float]:
        return (
            self.category_name,
            self.product_name,
            self.quantity,
            self.unit_price,
            self.price,
        )


def _get_product_name_from_row(row: Any) -> str:
    name_column = row.select(NAME_COLUMN_CLASS_PATTERN)[0]
    name_header = name_column.find(NAME_COLUMN_HEADER_TYPE)
    return name_header.contents[0]


def _get_quantity_from_row(row: Any) -> int:
    quantity_paragraph = row.select(QUANTITY_COLUMN_CLASS_PATTERN)[0]
    return _convert_quantity_paragraph(quantity_paragraph)


def _convert_quantity_paragraph(quantity_paragraph: Any) -> int:
    return int(quantity_paragraph.contents[0][1:])


def _get_price_from_row(row: Any) -> float:
    price_paragraph = row.select(PRICE_COLUMN_PATTERN)[0]
    return _convert_price_paragraph(price_paragraph)


def _convert_price_paragraph(price_paragraph: Any) -> float:
    return float(price_paragraph.contents[0][:-2])
