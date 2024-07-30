import pandas as pd
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Product, Category, Supplier, Stock
from .forms import ProductForm, CategoryForm, SupplierForm, StockUpdateForm
from .utils import send_low_stock_alert
import pytz

# Dashboard
def home(request):
    last_three_products = Product.objects.order_by('-id')[:3]
    return render(request, 'inventory/home.html', {'products': last_three_products})

# Bonus #import data
def import_data(request):
    if request.method == 'POST':
        product_csv = request.FILES.get('product_file')
        supplier_csv = request.FILES.get('supplier_file')
        category_csv = request.FILES.get('category_file')
        stock_csv = request.FILES.get('stock_file')
        
        if product_csv:
            import_products_from_csv(product_csv)
        if supplier_csv:
            import_suppliers_from_csv(supplier_csv)
        if category_csv:
            import_categories_from_csv(category_csv)
        if stock_csv:
            import_stock_from_csv(stock_csv)
        
        messages.success(request, 'Data imported successfully')
        return redirect('product_list')  

def export_data(request):
    if request.GET.get('export', '') == 'all':
        return export_all_data()
    return redirect('dashboard')

def make_tz_naive(series):
    return series.apply(lambda x: x.replace(tzinfo=None) if pd.notna(x) and hasattr(x, 'tzinfo') and x.tzinfo is not None else x)

def export_all_data():
    products = Product.objects.all().values(
        'name', 'description', 'price', 'category__name', 'suppliers__name', 'image'
    )
    df_products = pd.DataFrame(list(products))
    
    df_products['suppliers__name'] = df_products['suppliers__name'].apply(
        lambda x: ';'.join(x) if pd.notna(x) else ''
    )
    df_products['category__name'] = df_products['category__name'].apply(
        lambda x: x if pd.notna(x) else ''
    )

    # Export Suppliers
    suppliers = Supplier.objects.all().values()
    df_suppliers = pd.DataFrame(list(suppliers))

    categories = Category.objects.all().values()
    df_categories = pd.DataFrame(list(categories))

    stock_entries = Stock.objects.all().values(
        'product__name', 'quantity', 'date_updated'
    )
    df_stock = pd.DataFrame(list(stock_entries))
    
    df_stock['date_updated'] = make_tz_naive(df_stock['date_updated'])

    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = pd.ExcelWriter(response, engine='xlsxwriter')

    df_products.to_csv(response, index=False, header=True)
    df_suppliers.to_csv(response, index=False, header=True)
    df_categories.to_csv(response, index=False, header=True)
    df_stock.to_csv(response, index=False, header=True)

    return response

# Product Views
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    latest_stock_entry = product.stock_entries.order_by('-date_updated').first()
    return render(request, 'inventory/product_detail.html', {'product': product, 'latest_stock_entry': latest_stock_entry})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

def product_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            category__name__icontains=query
        ) | Product.objects.filter(
            suppliers__name__icontains=query
        )
    else:
        products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# Category Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})

# Supplier Views
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_confirm_delete.html', {'supplier': supplier})

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = supplier.products.all()
    return render(request, 'inventory/supplier_detail.html', {'supplier': supplier, 'products': products})

def supplier_inventory(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    products = Product.objects.filter(suppliers=supplier)
    return render(request, 'inventory/supplier_inventory.html', {'supplier': supplier, 'products': products})

#Stock Views
def stock_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            stock_entry, created = Stock.objects.get_or_create(
                product=product,
                defaults={'quantity': new_quantity}
            )
            if not created:
                stock_entry.quantity = new_quantity
                stock_entry.save()

            if product.stock_status() == "Low Stock":
                send_low_stock_alert(product.name, product.get_stock_level(), 'mohamedlimo236@gmail.com')
            return redirect('product_detail', pk=product.pk)
    else:
        form = StockUpdateForm()
    return render(request, 'inventory/stock_update.html', {'form': form, 'product': product})

def stock_status(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_status.html', {'products': products})

def stock_report(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_report.html', {'products': products})