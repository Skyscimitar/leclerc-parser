from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from .product_in_order import ProductInOrder

ORDER_FILE_PARSER = "html.parser"
ORDER_DETAILS_CLASS_PATTERN = "div[class$=_DetailCommande]"
ALL_SECTIONS_CLASS_PATTERN = "div[class$=_Accordeon]"
CATEGORY_NAME_HEADER_TYPE = "h3"
PRODUCT_ROW_TYPE = "tr"


@dataclass
class Order:

    order: BeautifulSoup
    columns = ["Category", "Name", "Quantity", "UnitPrice", "Price"]

    @classmethod
    def from_file(cls, file_path: Path):
        return cls(_get_parsed_order_from_file(file_path))

    def write_to_csv(self, file_path: Path):
        order_as_dataframe = self._convert_to_dataframe()
        order_as_dataframe.to_csv(str(file_path.resolve().absolute()), index=False)

    def _convert_to_dataframe(self) -> pd.DataFrame:
        order_details = _get_order_details(self.order)
        all_categories = _get_all_categories_from_order_details(order_details)
        order_rows = _get_all_products_in_order(all_categories)
        return pd.DataFrame(
            [product_in_order.to_tuple() for product_in_order in order_rows],
            columns=self.columns,
        )


def _get_parsed_order_from_file(file_path: Path) -> BeautifulSoup:
    order = _read_order_file(file_path)
    return BeautifulSoup(order, ORDER_FILE_PARSER)


def _read_order_file(file_path: Path) -> str:
    with open(str(file_path.resolve().absolute()), "r", encoding="utf-8") as order_file:
        order = order_file.read()
    return order


def _get_order_details(order: BeautifulSoup) -> Tag:
    return order.select(ORDER_DETAILS_CLASS_PATTERN)[0]


def _get_all_categories_from_order_details(order_details: Tag) -> Tag:
    return order_details.select(ALL_SECTIONS_CLASS_PATTERN)[0]


def _get_category_name(category: Tag) -> str:
    return category.find(CATEGORY_NAME_HEADER_TYPE).contents[0]


def _get_product_rows(products_in_category: Tag) -> ResultSet[Tag]:
    return products_in_category.find_all(PRODUCT_ROW_TYPE)


def _extract_products_from_category(
    category_name: str, products_in_category: Tag
) -> Sequence[ProductInOrder]:
    product_rows = _get_product_rows(products_in_category)
    return [
        ProductInOrder.from_row(category_name, product_row)
        for product_row in product_rows
    ]


def _get_all_products_in_order(all_categories: Tag) -> Sequence[ProductInOrder]:
    categories_and_products: ResultSet[Tag] = all_categories.find_all(
        "div", recursive=False
    )
    all_products_in_order = []
    for i in range(0, len(categories_and_products), 2):
        category_name = _get_category_name(categories_and_products[i])
        category_products = _extract_products_from_category(
            category_name, categories_and_products[i + 1]
        )
        all_products_in_order += category_products
    return all_products_in_order
