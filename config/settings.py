from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

# Data generation settings
GENERATION_CONFIG = {
    "seed": 42,
    "num_customers": 500,
    "num_products": 100,
    "num_orders": 2000,
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
}

# File names
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"
ORDERS_FILE = "orders.csv"
ORDER_ITEMS_FILE = "order_items.csv"