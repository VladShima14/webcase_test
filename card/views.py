from django.shortcuts import render, get_object_or_404
import json
from .models import Product, ProductDetail, Color, Size, Material
from django.http import HttpResponse
# Create your views here.


def index(request):
    products = Product.objects.all()

    return render(request, 'card/index.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_det = ProductDetail.objects.filter(product=product)
    colors = [product_detail.color.name for product_detail in product_det]
    sizes = [product_detail.size.name for product_detail in product_det]
    materials = [product_detail.material.name for product_detail in product_det]

    return render(request, 'card/detail.html', {'product': product,
                                              'product_det': product_det,
                                              'colors': list(set(colors)),
                                              'sizes': list(set(sizes)),
                                              'materials': list(set(materials))
                                              })


def color_price(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod')
        color_attr = request.GET.get('color')
        size_attr = request.GET.get('size')
        material_attr = request.GET.get('material')
        prod_det = ProductDetail.objects.filter(product=prod_id, color__name=color_attr,
                                                size__name=size_attr, material__name=material_attr)
        price_det = prod_det.values_list('price', flat=True)
        price = 0
        for i in price_det:
              price += i

        return HttpResponse(json.dumps({
            "price": str(price), }),
            content_type="application/json")



