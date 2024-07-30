from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
import os
import requests
from .models import Product, Category, Supplier, Stock
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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
    
    print("Columns in CSV:", data.columns.tolist())
    
    for index, row in data.iterrows():
        print(f"Processing row {index}: {row.to_dict()}")  
        
        category_name = row.get('category', None)
        if not category_name:
            print(f"Warning: 'category' is missing or empty in row {index}")
            continue
        category, _ = Category.objects.get_or_create(name=category_name)
        
        suppliers_str = row.get('suppliers', '')
        suppliers = [Supplier.objects.get_or_create(name=s.strip())[0] for s in suppliers_str.split(';') if s.strip()]

        image_url = row.get('image', None)
        image_file = None
        
        if image_url:
            try:
                if os.path.isfile(image_url):
                    with open(image_url, 'rb') as f:
                        image_content = ContentFile(f.read())
                else:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    image_content = ContentFile(response.content)
                
                file_name = os.path.basename(image_url)

                image_file = default_storage.save(f'product_images/{file_name}', image_content)
                
            except Exception as e:
                print(f"Failed to download or save image from URL {image_url}: {e}")

        product_data = {
            'name': row.get('name', ''),
            'description': row.get('description', ''),
            'price': row.get('price', 0),
            'category': category,
            'image': image_file,
        }
        

        product, created = Product.objects.update_or_create(name=row.get('name', ''), defaults=product_data)
        
        if suppliers:
            product.suppliers.set(suppliers) 
            product.save()

        print(f"Processed product: {product.name}")

def import_suppliers_from_csv(file):
    data = pd.read_csv(file)
    
    print("Columns in CSV:", data.columns.tolist())
    
    for index, row in data.iterrows():
        print(f"Processing row {index}: {row.to_dict()}")  # Print the row data for debugging
        
        supplier_data = {
            'name': row.get('name', ''),
            'address': row.get('address', ''),
            'logo': row.get('logo', None),
            'email': row.get('email', ''),
            'website': row.get('website', ''),
            'phone_number': row.get('phone_number', ''),
        }
        
        Supplier.objects.update_or_create(name=row.get('name', ''), defaults=supplier_data)
        print(f"Processed supplier: {supplier_data['name']}")

def import_categories_from_csv(file):
    data = pd.read_csv(file)
    
    print("Columns in CSV:", data.columns.tolist())
    
    for index, row in data.iterrows():
        print(f"Processing row {index}: {row.to_dict()}")  # Print the row data for debugging
        
        category_data = {
            'name': row.get('name', ''),
        }
        
        Category.objects.update_or_create(name=row.get('name', ''), defaults=category_data)
        print(f"Processed category: {category_data['name']}")
        
def import_stock_from_csv(file):
    data = pd.read_csv(file)
    
    print("Columns in CSV:", data.columns.tolist())
    
    for index, row in data.iterrows():
        print(f"Processing row {index}: {row.to_dict()}")  # Print the row data for debugging
        
        try:
            product = Product.objects.get(name=row.get('product', ''))
            stock_data = {
                'product': product,
                'quantity': row.get('quantity', 0),
                'date_updated': row.get('date_updated', None),
            }
            Stock.objects.create(**stock_data)
            print(f"Processed stock entry for product: {product.name}")
        except Product.DoesNotExist:
            print(f"Warning: Product '{row.get('product', '')}' not found in row {index}")
