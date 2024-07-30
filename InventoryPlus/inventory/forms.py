from django import forms
from .models import Product, Category, Supplier, Stock

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'suppliers', 'image']
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('This field is required.')
        return image

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        price = cleaned_data.get("price")
        category = cleaned_data.get("category")
        suppliers = cleaned_data.get("suppliers")
        
        if not name or not description or not price or not category or not suppliers:
            raise forms.ValidationError("All fields must be filled.")
        
        return cleaned_data
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'logo', 'email', 'website', 'phone_number']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'quantity']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }

