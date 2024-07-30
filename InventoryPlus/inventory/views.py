from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Category, Supplier, Stock
from .forms import ProductForm, CategoryForm, SupplierForm, StockForm, StockUpdateForm

# Dashboard
def dashboard(request):
    last_three_products = Product.objects.order_by('-id')[:3]
    return render(request, 'inventory/dashboard.html', {'products': last_three_products})

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

# Stock Views
def stock_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.product = product
            stock_entry.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = StockUpdateForm()
    return render(request, 'inventory/stock_update.html', {'form': form, 'product': product})

# View to show stock status
def stock_status(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_status.html', {'products': products})

# View to generate stock reports
def stock_report(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_report.html', {'products': products})
