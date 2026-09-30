import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

from config.settings import GENERATION_CONFIG, RAW_DATA_DIR
from src.data_generator.schemas import (
    CUSTOMER_COLUMNS,
    PRODUCT_COLUMNS,
    ORDER_COLUMNS,
    ORDER_ITEM_COLUMNS,
)


class EcommerceDataGenerator:
    """Reusable ecommerce data generator."""

    def __init__(self, config: dict = None):
        self.config = config or GENERATION_CONFIG
        self.fake = Faker()
        Faker.seed(self.config["seed"])
        random.seed(self.config["seed"])

        self.categories = [
            "Electronics", "Clothing", "Home", "Books",
            "Sports", "Beauty", "Toys", "Grocery"
        ]
        self.statuses = ["completed", "pending", "cancelled", "shipped"]

    def generate_customers(self) -> pd.DataFrame:
        customers = []
        for i in range(1, self.config["num_customers"] + 1):
            customers.append({
                "customer_id": i,
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.unique.email(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "country": "India",
                "signup_date": self.fake.date_between(start_date="-3y", end_date="today"),
            })
        return pd.DataFrame(customers, columns=CUSTOMER_COLUMNS)

    def generate_products(self) -> pd.DataFrame:
        products = []
        for i in range(1, self.config["num_products"] + 1):
            price = round(random.uniform(100, 5000), 2)
            cost = round(price * random.uniform(0.4, 0.7), 2)
            products.append({
                "product_id": i,
                "product_name": self.fake.catch_phrase(),
                "category": random.choice(self.categories),
                "price": price,
                "cost": cost,
            })
        return pd.DataFrame(products, columns=PRODUCT_COLUMNS)

    def generate_orders_and_items(self, customers: pd.DataFrame, products: pd.DataFrame):
        orders = []
        order_items = []
        order_item_id = 1

        start_date = datetime.strptime(self.config["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(self.config["end_date"], "%Y-%m-%d")
        date_range = (end_date - start_date).days

        for order_id in range(1, self.config["num_orders"] + 1):
            customer_id = int(customers.sample(1)["customer_id"].values[0])
            order_date = start_date + timedelta(days=random.randint(0, date_range))
            status = random.choices(self.statuses, weights=[0.7, 0.1, 0.1, 0.1])[0]

            num_items = random.randint(1, 5)
            selected_products = products.sample(num_items)
            total_amount = 0

            for _, product in selected_products.iterrows():
                quantity = random.randint(1, 3)
                unit_price = product["price"]
                line_total = round(quantity * unit_price, 2)
                total_amount += line_total

                order_items.append({
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": int(product["product_id"]),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total,
                })
                order_item_id += 1

            orders.append({
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.date(),
                "status": status,
                "total_amount": round(total_amount, 2),
            })

        orders_df = pd.DataFrame(orders, columns=ORDER_COLUMNS)
        order_items_df = pd.DataFrame(order_items, columns=ORDER_ITEM_COLUMNS)
        return orders_df, order_items_df

    def generate_all(self) -> dict:
        print("Generating customers...")
        customers = self.generate_customers()

        print("Generating products...")
        products = self.generate_products()

        print("Generating orders and order items...")
        orders, order_items = self.generate_orders_and_items(customers, products)

        return {
            "customers": customers,
            "products": products,
            "orders": orders,
            "order_items": order_items,
        }

    def save_to_csv(self, data: dict, output_dir: Path = None):
        output_dir = output_dir or RAW_DATA_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        for name, df in data.items():
            file_path = output_dir / f"{name}.csv"
            df.to_csv(file_path, index=False)
            print(f"Saved: {file_path} ({len(df)} records)")