import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.data_generator.generator import EcommerceDataGenerator


def main():
    print("Starting ecommerce data generation...")
    generator = EcommerceDataGenerator()
    data = generator.generate_all()
    generator.save_to_csv(data)
    print("Data generation completed successfully.")


if __name__ == "__main__":
    main()