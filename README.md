# 🗃️ Inventory Management System

A robust **Inventory Management System** built using **Django** (MTV pattern) for managing products, categories, suppliers, and stock levels. This system includes search, reporting, CSV import/export, and smart alerts for low stock and upcoming expiries.

## 🚀 Features

- ✅ Product, Category, and Supplier Management  
- 📦 Stock Tracking with Quantity Updates  
- 🔎 Search & Filter for Products and Suppliers  
- 📉 Low Stock & Expiry Alerts  
- 📊 Reports (Stock Levels, Supplier Info, Expiry Lists)  
- 📥📤 CSV Import and Export Support

## 🛠️ Tech Stack

- **Backend:** Django (MTV Architecture)  
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)  
- **Frontend:** Django Templates + Bootstrap (optional)  

## 📁 Project Structure

```
inventory_system/
├── inventory/              # App containing core logic
│   ├── models.py           # Models for Product, Category, Supplier
│   ├── views.py            # Views handling data and rendering
│   ├── templates/          # HTML templates for UI
│   ├── forms.py            # Django forms for CRUD
│   └── urls.py             # App-level URL routes
├── inventory_system/       # Project settings and config
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## 🧪 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Migrations**

```bash
python manage.py migrate
```

5. **Create a Superuser**

```bash
python manage.py createsuperuser
```

6. **Run the Server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📌 Future Improvements

- Barcode Scanner Integration  
- Role-based Access (Admin, Staff)  
- REST API for external systems  
- Dashboard with charts and KPIs  

## 📄 License

MIT License

## ⚙️ Detailed Functionalities

### 🧾 Product Management
- Add, edit, and delete product entries with attributes like name, SKU, description, category, price, quantity, and expiry date.
- Associate each product with a category and a supplier.
- Upload products in bulk via CSV import.

### 🗂️ Category Management
- Create and manage product categories for better organization.
- Categories are used for filtering and reporting purposes.

### 👤 Supplier Management
- Add and manage supplier profiles with contact information and supplied products.
- View products linked to a particular supplier.
- Generate supplier-wise reports for stock levels and transaction history.

### 📦 Stock Management
- Monitor and update stock quantities manually or automatically via CSV.
- Visual indicators for low stock thresholds.
- Track stock movement and history for auditing.

### 🛎️ Alerts and Notifications
- Automatic alerts for products that are low in stock (below a set threshold).
- Expiry date tracking and alerting for soon-to-expire or expired products.

### 🔍 Search and Filter
- Real-time search bar for filtering products by name, category, supplier, or status.
- Advanced filters for expiry, quantity, and category-based searches.

### 📊 Reports
- Generate on-demand reports for:
  - Current inventory levels
  - Low-stock items
  - Expiring or expired products
  - Supplier-wise stock reports
- Export reports as downloadable CSV files.

### 🔄 CSV Import/Export
- Bulk import products or suppliers from a CSV file.
- Export current inventory or supplier details for external use.

### 🧑‍💼 Admin Interface
- Built-in Django admin panel for backend operations.
- Manage users, permissions, and database entries through an intuitive UI.
