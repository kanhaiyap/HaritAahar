import json
from datetime import datetime
from django.core.management.base import BaseCommand
from shop.models import Product, Category

class Command(BaseCommand):
    help = 'Import products from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        json_file_path = 'shop/static/products.json'

        with open(json_file_path, 'r') as file:
            products_data = json.load(file)

        for product_data in products_data:
            # Ensure category_name is split if it's a comma-separated string
            category_names = product_data.get('category_name', [])
            if isinstance(category_names, str):
                # Split by comma and remove any extra spaces
                category_names = [category.strip() for category in category_names.split(',')]

            categories = []
            for category_name in category_names:
                # Fetch or create categories using category_name
                category, created = Category.objects.get_or_create(name=category_name)
                categories.append(category)

            # Convert the expiry_date to the correct format (YYYY-MM-DD)
            expiry_date_str = product_data.get('expiry_date', '2025-01-01')
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                expiry_date = '2025-01-01'  # Default value if conversion fails

            # Create or update the product
            product, created = Product.objects.update_or_create(
                product_name=product_data['product_name'],
                defaults={
                    'name': product_data.get('product_name', 'Unnamed Product'),
                    'price': product_data.get('price', 0.0),
                    'description': product_data.get('description', 'No description available'),
                    'product_description': product_data.get('product_description', 'No product description'),
                    'brand': product_data.get('brand', 'N/A'),
                    'color': product_data.get('color', 'N/A'),
                    'size': product_data.get('size', 'N/A'),
                    'quantity': product_data.get('quantity', 0),
                    'availability': product_data.get('availability', True),
                    'rating': product_data.get('rating', 0.0),
                    'reviews': product_data.get('reviews', 0),
                    'expiry_date': expiry_date,  # Use the converted expiry date
                    'shipping_cost': product_data.get('shipping_cost', 0.0),
                    'seller_name': product_data.get('seller_name', 'Unknown Seller'),
                    'seller_rating': product_data.get('seller_rating', 0.0),
                }
            )

            # After saving the product, update the ManyToManyField (category_name)
            if categories:
                # Use `set()` to assign categories to the product
                product.category_name.set(categories)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Product "{product.name}" created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Product "{product.name}" updated'))
