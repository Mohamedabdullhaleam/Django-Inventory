from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from .models import Product, Category, Supplier, Stock

def send_low_stock_alert(product_name, current_stock_level, manager_email):
    subject = f'Low Stock Alert: {product_name}'
    message = f'The stock level for "{product_name}" is currently at {current_stock_level}. Please review the inventory.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [manager_email],
        fail_silently=False,
    )
def import_products_from_csv(file):
    data = pd.read_csv(file)
    for _, row in data.iterrows():
        category, _ = Category.objects.get_or_create(name=row['category'])
        suppliers = [Supplier.objects.get_or_create(name=s)[0] for s in row['suppliers'].split(';') if s]
        product_data = {
            'name': row['name'],
            'description': row['description'],
            'price': row['price'],
            'category': category,
            'suppliers': suppliers,
            'image': row['image'] if pd.notna(row['image']) else None,
        }
        Product.objects.update_or_create(name=row['name'], defaults=product_data)

def import_suppliers_from_csv(file):
    data = pd.read_csv(file)
    for _, row in data.iterrows():
        Supplier.objects.update_or_create(
            name=row['name'],
            defaults={
                'address': row['address'],
                'logo': row['logo'] if pd.notna(row['logo']) else None,
                'email': row['email'],
                'website': row['website'],
                'phone_number': row['phone_number']
            }
        )

def import_categories_from_csv(file):
    data = pd.read_csv(file)
    for _, row in data.iterrows():
        Category.objects.get_or_create(name=row['name'])

def import_stock_from_csv(file):
    data = pd.read_csv(file)
    for _, row in data.iterrows():
        product = Product.objects.get(name=row['product'])
        Stock.objects.update_or_create(
            product=product,
            date_updated=row['date_updated'] if pd.notna(row['date_updated']) else None,
            defaults={'quantity': row['quantity']}
        )
