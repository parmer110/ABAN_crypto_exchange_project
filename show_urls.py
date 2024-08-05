import os
import sys
import django

from django.conf import settings
from django.urls import get_resolver, URLPattern, URLResolver

def show_urls(urls=None, depth=0):
    if urls is None:
        urls = get_resolver().url_patterns

    for url in urls:
        if isinstance(url, URLPattern):
            print(f"{'  ' * depth}{url.pattern}")
        elif isinstance(url, URLResolver):
            print(f"{'  ' * depth}{url.pattern}/")
            show_urls(url.url_patterns, depth + 1)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_exchange.settings')
    django.setup()
    show_urls()
