from django.core.mail import send_mail
from django.conf import settings

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
