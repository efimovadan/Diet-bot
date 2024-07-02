from .db import Database
from models import Product

class ProductRepository:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._db = Database()
            cls._instance = super(ProductRepository, cls).__new__(cls)
        return cls._instance

    async def get_products_by_names(self, names: list[str]) -> list[Product]:
        placeholders = ', '.join(f'${i+1}' for i in range(len(names)))
        query = f"SELECT name, proteins, fats, carbs, calories FROM products WHERE name ILIKE ANY(ARRAY[{placeholders}])"
        patterns = [f'%{name}%' for name in names]
        product_data = await self._db.execute_query(query, params=patterns, return_type='fetch')
        products = []
        for row in product_data:
            products.append(Product(
                name=row['name'],
                proteins=row['proteins'],
                fats=row['fats'],
                carbs=row['carbs'],
                calories=row['calories']
            ))
        return products
    
    async def get_products(self) -> list[Product]:
        query = "SELECT name, proteins, fats, carbs, calories FROM products"
        product_data = await self._db.execute_query(query, return_type='fetch')
        products = [Product(name=row['name'], proteins=row['proteins'], fats=row['fats'], carbs=row['carbs'], calories=row['calories']) for row in product_data]
        return products