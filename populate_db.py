import os
import django
import random
from faker import Faker
from decimal import Decimal
from django.utils.text import slugify

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomstore.settings")  # Change 'your_project' to your project name
django.setup()

from store.models import Category, Product  # Change 'your_app' to your app name

# Initialize Faker
fake = Faker()

# Create Categories
def create_categories(n=5):
    categories = []
    for _ in range(n):
        name = fake.word().capitalize() + " Category"
        slug = slugify(name)
        category, created = Category.objects.get_or_create(name=name, slug=slug)
        categories.append(category)
    return categories

# Create Products
def create_products(n=50):
    categories = create_categories()
    for _ in range(n):
        title = fake.sentence(nb_words=3)
        brand = fake.company()
        description = fake.paragraph(nb_sentences=3)
        slug = slugify(title)
        price = Decimal(random.uniform(10.00, 99.99)).quantize(Decimal("0.01"))
        # image = "images/default.jpg"  # Use a placeholder image or update accordingly
        category = random.choice(categories)

        Product.objects.create(
            title=title,
            brand=brand,
            description=description,
            slug=slug,
            price=price,
            # image=image,
            category=category,
        )

# Run the script
if __name__ == "__main__":
    print("Seeding database with categories and products...")
    create_products()
    print("Database seeding complete!")
