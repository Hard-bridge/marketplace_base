from django.shortcuts import render, redirect
from .forms import Reg, Auth
from  .models import User, Product, Order, Review

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def auth(request):
    form = Auth()
    error = ''
    if request.method == 'POST':
        if User.objects.filter(login=request.POST['login'], password= request.POST['password']).exists():
            request.session['user'] = request.POST['login']
            return redirect('/panel')
        else:
            error = 'Логин и/или пароль не существуют!!'

    return render(request, 'auth.html', {'form': form})
def reg(request):
    form = Reg()
    suc = ''
    error = ''
    if request.method == 'POST':
        if User.objects.filter(login=request.POST['login']).exists():
            error = 'Такой логин уже существует!'
        else:
            user = User()
            user.login = request.POST['login']
            user.password = request.POST['password']
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.balance = 0
            user.save()
            suc = 'Успешная регистрация!'
    return render(request, 'reg.html', {'form': form, 'suc': suc, 'error': error})


def panel(request):
    m = False
    if 'user' in request.session:
        m = True
        current_user = User.objects.filter(login=request.session['user']).first()
        current_order = Order.objects.filter(user=current_user)
        return render(request, 'panel.html', {'current_user': current_user, 'current_order': current_order, 'm':m})

    else:
        return render(request, 'panel.html', {'m': m})


def payOrder(request):
    current_user = User.objects.filter(login=request.session['user']).first()
    id_order = request.POST['id_order']
    order = Order.objects.get(id=id_order)
    if order.status == 'Не оплачен' and current_user.balance >= order.total_price:
        order.status = 'Оплачен'
        order.save()
        current_u = User.objects.get(login=request.session['user'])

        current_u.balance = current_u.balance  - order.total_price
        current_u.save()

    return redirect('/panel')

def addcart(request):
    id_product = request.POST['id_product']
    count = request.POST.get('count', 1)
    if 'basket' in request.session:
        for n in range(int(count)):
            id_pr = request.session['basket']
            request.session['basket'] = id_pr + ',' + id_product
    else:
        for n in range(int(count)):
            if n == 0:
                request.session['basket'] = id_product
            else:
                id_pr = request.session['basket']
                request.session['basket'] = id_pr + ',' + id_product
    return redirect('/')

def cart(requst):
    products = []
    total_price_cart = 0
    if 'basket' in requst.session:
        cart = requst.session['basket']
        cart_id = cart.split(',')
        products_n = {}
        for id in cart_id:
            if id != '':
                id = int(id)
                if id in products_n:
                    products_n[id] += 1
                else:
                    products_n[id] = 1
        for key, value in products_n.items():
            products.append({
                'id': key,
                'count': value,
                'product': Product.objects.filter(id=int(key)).first(),
                'total_price': value * Product.objects.filter(id=int(key)).first().price
            })
            total_price_cart += (value * Product.objects.filter(id=int(key)).first().price)
    return render(requst, 'cart.html', {'products': products, 'total_price_cart': total_price_cart})

def changecount(request):
    id_product = request.POST['id_product']
    count = request.POST['count']
    if int(count) < 1:
        return redirect('/cart')
    if 'basket' in request.session:
        cart = request.session['basket']
        cart_id = cart.split(',')
        res_basket = []
        for id in cart_id:
            if id != '':
                if id != str(id_product):
                    res_basket.append(id)
        request.session['basket'] = ','.join(res_basket)

        res_b = []
        for i in range(int(count)):
            res_b.append(str(id_product))
        request.session['basket'] += ','+','.join(res_b)
    return redirect('/cart')



def addOrder(request):
    products = []
    total_price_cart = 0
    if 'basket' in request.session:
        cart = request.session['basket']
        cart_id = cart.split(',')
        products_n = {}
        for id in cart_id:
            if id != '':
                id = int(id)
                if id in products_n:
                    products_n[id] += 1
                else:
                    products_n[id] = 1
        for key, value in products_n.items():
            products.append({
                'id': key,
                'count': value,
                'product': Product.objects.filter(id=int(key)).first(),
                'total_price': value * Product.objects.filter(id=int(key)).first().price
            })
            total_price_cart += (value * Product.objects.filter(id=int(key)).first().price)
    pr_id = []

    order = Order()
    order.user = User.objects.filter(login=request.session['user']).first()
    order.total_price = total_price_cart
    for product in products:
        pr_id.append(product['product'].id)
    products_new = Product.objects.filter(id__in=pr_id)
    order.save()
    order.products.add(*products_new)

    del request.session['basket']
    return redirect('/panel')


def cartdel(request):
    id_product = request.POST['id_product']
    if 'basket' in request.session:
        cart = request.session['basket']
        cart_id = cart.split(',')
        id_cart = ''
        for i in cart_id:
            if i != id_product:
                id_cart += (i + ',')
        request.session['basket'] = id_cart[:-1]
    return redirect('/cart')

def catalog(request):
    sort = request.GET.get('sort', '')
    sort_value = request.GET.get('sort_value', '')
    products = Product.objects.all()
    if sort and sort_value:
        if sort.lower() == 'asc':
            products = products.order_by(sort_value)
        elif sort.lower() == 'desc':
            products = products.order_by('-' + sort_value)

    return render(request, 'catalog.html', {'products': products})

def detail(request, id_product):
    product = Product.objects.filter(id=id_product).first()
    return render(request, 'detailt.html', {'product': product})

def addreviews(request):
    if request.method == 'POST':
        data = request.POST
        id_product = data['id_product']
        review = data['review']
        current_user = User.objects.filter(login=request.session['user']).first()
        current_product = Product.objects.filter(id=id_product).first()

        r = Review()
        r.user_id = current_user
        r.product_id = current_product
        r.text = review
        r.save()
    return redirect('/panel')