import json
import urllib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from mainwebsite.models import *

from django.core.files.storage import FileSystemStorage


def homePage(request):
    data = {
        "artists": Artists.objects.all()
    }
    return render(request, "mainwebsite/homepage.html", data)


def artistsListPage(request):
    data = {
        "artists": Artists.objects.all()
    }
    return render(request, "mainwebsite/artistsList.html", data)


def artistPage(request, id):
    data = {
        "artist": Artists.objects.get(id=id),
        "size": ArtworkSize.objects.all()
    }
    return render(request, "mainwebsite/artist_page.html", data)


def productDetailsPage(request, id):
    data = {
        "artwork": Artwork.objects.get(id=id),
        "size": ArtworkSize.objects.all()
    }
    return render(request, "mainwebsite/product_details.html", data)


def cartPage(request):
    data = {}
    try:
        data["empty_cart"] = False
        if "cartHistory" in request.COOKIES:
            data["cookie_present"] = True
        cartHistory = json.loads(urllib.parse.unquote(request.COOKIES["cartHistory"]))
        cartItems = cartHistory["cartItems"]
        total_price = 0
        cartDataToSend = []
        for i in cartItems:
            product_record = Artwork.objects.get(id=i["productId"])
            size_record = ArtworkSize.objects.get(size=i["size"])
            total_price += size_record.price * i["quantity"]

            cartDataToSend.append({
                "product" : product_record,
                "size" : size_record,
                "price" : size_record.price * i["quantity"],
                "quantity" : i["quantity"]
            })

        data["total_price"] = total_price
        data["cart_data"] = cartDataToSend
    except:
        data["empty_cart"] = True
        data["total_price"] = 0
    return render(request,"mainwebsite/cart_page.html",data)

# Normal Function
def generate_random_filename(filename):
    extension = str(filename).split(".")[-1]
    random_name = str(random.randint(1111111111111111,9999999999999999))
    final_random_name = random_name+"."+extension
    return final_random_name


def checkoutPage(request):
    data = {}
    try:
        data["empty_cart"] = False
        if request.method == "POST" and "kettodetails" in request.FILES:

            screenshot = request.FILES["kettodetails"]
            fs = FileSystemStorage(location='media/')
            filename = fs.save(generate_random_filename(screenshot.name), screenshot)
            screenshotFinalName = fs.generate_filename(filename)

            cartHistory = json.loads(urllib.parse.unquote(request.COOKIES["cartHistory"]))
            cartItems = cartHistory["cartItems"]
            total_price = 0
            cartDataToSend = []
            for i in cartItems:
                product_record = Artwork.objects.get(id=i["productId"])
                size_record = ArtworkSize.objects.get(size=i["size"])
                total_price += size_record.price * i["quantity"]

                cartDataToSend.append({
                    "product": product_record.id,
                    "size": size_record.size,
                    "price_per_product" : size_record.price,
                    "price": size_record.price * i["quantity"],
                    "quantity": i["quantity"]
                })

            order_record = OrderHistory.objects.create(
                ketto_transaction_details=screenshotFinalName,
                customer_name=request.POST.get("customer_name",""),
                customer_phoneNo=request.POST.get("phoneno",""),
                customer_email=request.POST.get("email",""),
                customer_address=request.POST.get("address",""),
                customer_pinCode=request.POST.get("pincode",""),
                order_details=cartDataToSend,
                total_price=total_price
            )
            response = redirect(f"/success-order/{order_record.order_id}/")
            response.delete_cookie("cartHistory")
            return response




        if "cartHistory" in request.COOKIES:
            data["cookie_present"] = True
        cartHistory = json.loads(urllib.parse.unquote(request.COOKIES["cartHistory"]))
        cartItems = cartHistory["cartItems"]
        total_price = 0
        cartDataToSend = []
        for i in cartItems:
            product_record = Artwork.objects.get(id=i["productId"])
            size_record = ArtworkSize.objects.get(size=i["size"])
            total_price += size_record.price * i["quantity"]

            cartDataToSend.append({
                "product" : product_record,
                "size" : size_record,
                "price" : size_record.price * i["quantity"],
                "quantity" : i["quantity"]
            })

        data["total_price"] = total_price
        data["cart_data"] = cartDataToSend

    except Exception as e:
        print(e)
        data["empty_cart"] = True
        data["total_price"] = 0

    return render(request,"mainwebsite/checkout_page.html",data)


def aboutPage(request):
    return render(request,"mainwebsite/about_page.html")

def successPage(request,order_id):
    data = {
        "order_id" : order_id
    }
    return render(request,"mainwebsite/success_order.html",data)


def orders_search(request):
    if not request.user.is_authenticated:
        return HttpResponse("401 Unauthorized",status=401)
    data = {}

    orders = OrderHistory.objects.all().order_by("-id")

    if "order_id" in request.GET:
        data["order_id"] = request.GET["order_id"]
        orders = orders.filter(order_id=request.GET["order_id"])
    elif "email_id" in request.GET:
        data["email_id"] = request.GET["email_id"]
        orders = orders.filter(customer_email__icontains=request.GET["email_id"])
    elif "mobile_no" in request.GET:
        data["mobile_no"] = request.GET["mobile_no"]
        orders = orders.filter(customer_phoneNo__contains=request.GET["mobile_no"])
    elif "customer_name" in request.GET:
        data["customer_name"] = request.GET["customer_name"]
        orders = orders.filter(customer_name__contains=request.GET["customer_name"])

    data["orders"] = orders
    return render(request,"mainwebsite/order_details.html",data)


def orders_details(request, order_id):
    print(order_id)
    if not request.user.is_authenticated:
        return HttpResponse("401 Unauthorized",status=401)
    data = {}
    order_record = OrderHistory.objects.get(order_id=order_id)
    data["order_record"] = order_record
    order_history = []

    for i in order_record.order_details:
        product_record = Artwork.objects.get(id=i["product"])
        order_history.append({
            "product_id" : product_record.id,
            "artist_id" : product_record.artist_id,
            "artist_name" : product_record.artist.name,
            "product_image_path" : product_record.picture.path,
            "product_image_link" : product_record.picture.url,
            "size" : i["size"],
            "price_per_product" : i["price_per_product"],
            "quantity" : i["quantity"],
            "total_price" : i["price_per_product"]*i["quantity"]
        })
    data["order_history"] = order_history
    return render(request,"mainwebsite/single_order_details.html",data)