from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Review , Contact,Post
from django.views.generic import  DetailView
from cart.forms import CartAddProductForm
from django.contrib import messages
from datetime import datetime
from django.template import RequestContext
from django.http import HttpResponse
 



def index(request):
    top_five_products = Product.objects.all()[:8]
    categories = Category.objects.all()[:6]
    products = Product.objects.all().order_by('-id')[:6]
    blog = Post.objects.all().order_by("-id")[:6]
    time_now = datetime.now()
    time = {
        'now': time_now.strftime("%H:%M")
    }
    return render(request,'bookshop/index.html',{'categories':categories,'products':products,'top_five_products':top_five_products,'time':time['now'],'blog':blog})

    
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    return render(request,'bookshop/products_list.html',{'category':category,
                                                     'categories':categories,
                                                     'products':products})
   

def product_detail(request, slug):
    product = get_object_or_404(Product,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    reviewproduct = Product.objects.filter(slug=slug)
    prid = None
    for product_id in reviewproduct:
        prid = product_id.id

    all_reviews = Review.objects.filter(product=prid)
    
    return render(request,'bookshop/product_detail.html',{'product': product,'cart_product_form': cart_product_form,'all_reviews':all_reviews})

def all_Categories(request):
    categories = Category.objects.all()
    return render(request,'bookshop/all_category_list.html',{'categories':categories})



def contact_us(request):
    if request.method == 'POST':
        n = request.POST['Name']
        e = request.POST['Email']
        m = request.POST['Message']
        Contact.objects.create(name=n, email=e,message=m)
        print('*'*50)
    else:
        print('#'*10)   
    return render(request,'bookshop/contact_us.html')


def search_Result(request):
    if request.method== 'POST':
        searh_query = request.POST['search']
        query_result = Product.objects.filter(name__startswith=searh_query)
        return render(request,'bookshop/search.html',{'query_result':query_result,'searh_query':searh_query})

def Comment_Review(request,product_id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        rating = request.POST['rating']
        review_comment = request.POST['review']
        product = get_object_or_404(Product,id=product_id)
        comment_review = Review.objects.create(product=product,name=name,email=email,rating=rating,review_comment=review_comment)
        message = messages.success(request,"コメントが送信されました")  
        return render(request,'bookshop/product_detail.html')
