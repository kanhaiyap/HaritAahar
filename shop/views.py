import os
from pathlib import Path
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import Order, Payment, Product, Category, Address, Orders
from .forms import AddressForm, ContactForm, CustomUserCreationForm, UserRegistrationForm
from .utils import send_otp_via_whatsapp
from django.templatetags.static import static
import json


from .forms import ProductSearchForm
# from django import template

# register = template.Library()

# @register.filter(name='get_item')
# def get_item(dictionary, key):
#     return dictionary.get(key)
def home(request):
    # Path to the categories image folder
    categories_dir = Path(settings.BASE_DIR) / "shop" / "static" / "images" / "categories"
    
    # Get all image files in the categories folder
    category_images = {}
    for image in os.listdir(categories_dir):
        if image.endswith(('.jpeg', '.jpg', '.png')):
            # Extract the category name (without extension)
            category_name = image.split('.')[0].replace('-', ' ').title()
            category_images[category_name] = f"images/categories/{image}"

    slides_dir = Path(settings.BASE_DIR) / "shop" / "static" / "images" / "slides"
    
    # Get all image files in the slides folder
    slide_images = []
    for image in os.listdir(slides_dir):
        if image.endswith(('.jpeg', '.jpg', '.png')):
            slide_images.append(f"images/slides/{image}")
    
    # Prepare the context to pass to the template
    context = {
        'category_images': category_images,
        'slide_images': slide_images,
    }

    # Prepare the context to pass to the template
  

    return render(request, 'home.html', context)


from .models import Product 


# Update the get_products_by_category function to return products directly
def get_products_by_category(request, category):
    products = Product.objects.filter(category_name=category)  # Filter products based on the category
    print(products)  # Optional: print the products for debugging
    return products  # Return the filtered products


def product_page(request, category):
    # Load data from the JSON file
    json_path = Path(settings.BASE_DIR) / "shop/static/products.json"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []  # In case the JSON file is empty or malformed
    except FileNotFoundError:
        data = []  # In case the file is not found
    
    # Filter the data based on the requested category
    filtered_products = []
    for product in data:
        if category in product["category_name"]:
            # Generate the image URL from product_name
            image_name = product["product_name"].lower().replace(" ", "_")  # Convert to lowercase and replace spaces with underscores
            product_image_url = static(f'images/products/{image_name}.jpg')  # Assuming images are named like 'banana.jpg'
            
            # Add the image URL to the product
            product["image_url"] = product_image_url
            filtered_products.append(product)

    context = {
        'category': category,
        'products': filtered_products
    }

    return render(request, 'product_page.html', context)
    
def load_images(request):
    # Define the path where images are stored
    image_folder = os.path.join(settings.BASE_DIR, 'shop', 'static', 'images', 'img')

    # Get a list of image files in the directory
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jfif', '.jpg', '.png'))]

    # Render the template and pass the list of image file names
    return render(request, 'index.html', {'image_files': image_files})

import json
def product_list(request):
    products = []
    json_path = Path(settings.BASE_DIR) / "shop/static/products.json"  # Path to the JSON file
    image_folder = Path(settings.BASE_DIR) / "shop/static/images/products"  # Path to the image folder

    # Load data from JSON file
    with open(json_path, encoding='utf-8') as jsonfile:
        product_data = json.load(jsonfile)
        
        for product in product_data:
            product_id = product['product_name']
            image_path = f"images/products/{product_id}.jpeg"  # Default to .jpeg format
            
            # Check if .jpeg exists, fallback to .jpg if not
            if not (image_folder / f"{product_id}.jpeg").exists():
                if (image_folder / f"{product_id}.jpg").exists():
                    image_path = f"images/products/{product_id}.jpg"

            products.append({
                'name': product['product_name'],
                'id': product['product_name'],
                'price': product['price'],
                'image': image_path,  # Dynamically determined image path
            })

    return render(request, 'products.html', {'products': products})


def about(request):
    return render(request, 'about.html')






@login_required  # This ensures the user is logged in before accessing the profile page
def profile(request):
    # Fetch the orders related to the logged-in user
    orders = Order.objects.filter(user=request.user)  # Adjust this based on your order model and relationship

    # Prepare the context to send to the template
    context = {
        'user': request.user,
        'orders': orders,
    }

    return render(request, 'account/profile.html', context)




from .forms import ContactForm
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            subject = f"Message from {name}"
            body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            recipient_email = 'your-email@example.com'  # Your email to receive the contact form submission
            
            send_mail(subject, body, email, [recipient_email])

            return HttpResponse('Thank you for contacting us! We will get back to you soon.')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def cart(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Fetch cart items from the session
        cart_items = request.session.get('cart', {})
        
        # Fetch user-specific addresses
        addresses = Address.objects.filter(user=request.user)
        
        # Render the cart page
        return render(request, 'cart.html', {'cart_items': cart_items, 'addresses': addresses})
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')


def manage_address(request):
    # Get the user's current address or create a new one if it doesn't exist
    address, created = Address.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('cart')  # Redirect to cart or another page after saving
    else:
        form = AddressForm(instance=address)

    return render(request, 'manage_address.html', {'form': form})









otp_cache = {}


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Extract phone number and other details
            phone_number = form.cleaned_data.get('phone_number')
            otp = send_otp_via_whatsapp(phone_number)

            # Cache OTP for verification
            otp_cache[phone_number] = otp

            # Temporarily store form data in session
            request.session['signup_form_data'] = form.cleaned_data
            request.session['phone_number'] = phone_number

            # Redirect to OTP verification page
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')
        entered_otp = request.POST.get('otp')

        # Check OTP
        if phone_number in otp_cache and otp_cache[phone_number] == int(entered_otp):
            # OTP verified; save the user
            signup_form_data = request.session.get('signup_form_data')

            if signup_form_data:
                # Save user details from session data
                form = CustomUserCreationForm(signup_form_data)
                if form.is_valid():
                    user = form.save()
                    messages.success(request, 'Account created successfully!')
                    
                    # Clean up session data
                    del request.session['signup_form_data']
                    del otp_cache[phone_number]

                    return redirect('login')
            else:
                messages.error(request, 'Session expired. Please sign up again.')
                return redirect('signup')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Replace 'home' with your desired redirect page.
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')



import random
from twilio.rest import Client

def send_otp_via_whatsapp(phone_number):
    # Twilio credentials
    account_sid = 'ACe2351ba25db4d30c3661c3cc41ec975c'
    auth_token = 'd23684d056e79343ebb8da0dcc8da60a'

    whatsapp_from = 'whatsapp:+16204458588'  # Twilio's WhatsApp sandbox number

    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)

    # Create Twilio client
    client = Client(account_sid, auth_token)

    # Send OTP via WhatsApp
    message = client.messages.create(
        body=f"Your Harit Aahar OTP is: {otp}. Please use this to verify your account.",
        from_=whatsapp_from,
        to=f'whatsapp:{phone_number}'  # Ensure the number is in E.164 format
    )

    # Return the OTP for verification
    return otp







razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def create_order(request):
    if not request.user.is_authenticated:
        # If the user is not logged in, redirect to login page
        return redirect('login') 
    if request.method == 'GET':
        # Debugging: Print the request.GET to verify the total_price
        print(f"Request GET data: {request.GET}")
        
        total_price = request.GET.get('total_price')
        
        if not total_price:
            print("Total price is missing!")
            return redirect('/')  # Redirect to home if total_price is not provided

        try:
            total_price = int(float(total_price)*100 ) # Convert to float
        except ValueError:
            print(f"Invalid total_price value: {total_price}")
            return redirect('/')  # Handle invalid total_price value

        user = request.user  # Get the logged-in user
        # Create an order in your system
        order = Order.objects.create(user=user, total_price=total_price, status='Pending')

        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': total_price,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1',
        })

        # Save Razorpay order ID
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        # Render the payment page with Razorpay order details
        return render(request, 'payment_page.html', {'order': order, 'razorpay_order': razorpay_order})

    # If POST request or invalid, redirect
    return redirect('/')





razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def verify_payment(request):
    # Print request data for debugging
    print(request.GET)
    print(request.POST)

    # Check if Razorpay is sending the data via GET or POST
    if request.method == 'GET':
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature')
    else:
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

    # Check if any of the required values are missing
    if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
        return HttpResponse("Missing payment details", status=400)

    # Verify the payment signature with Razorpay
    try:
        razorpay_client.payment.fetch(razorpay_payment_id).verify_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        # Payment is successful, update the payment status
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.status = 'Paid'
        order.save()

        # Create a payment record
        payment = Payment.objects.create(
            order=order,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_order_id=razorpay_order_id,
            payment_status='Success'
        )

        return JsonResponse({'status': 'success'})

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'status': 'failed'}, status=400)
    









def orders_page(request):
    # Fetching all orders
    orders = Orders.objects.all()  # Get all orders from the database

    # Debugging: print the orders to the console
    print("Orders:", orders)  # You should see the order data in the console

    return render(request, 'orders.html', {'orders': orders})


def fulfill_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    order.is_fulfilled = True
    order.save()
    return redirect('orders_page')

def resolve_issue(request, order_id):
    order = Orders.objects.get(id=order_id)
    order.issue_status = 'resolved'
    order.save()
    return redirect('orders_page')

from django.shortcuts import get_object_or_404, redirect


def mark_paid(request, order_id):
    # Get the order or return 404 if not found
    order = get_object_or_404(Orders, id=order_id)
    
    # Update payment status
    order.payment_status = 'paid'
    order.save()

    # Redirect back to orders page
    return redirect('orders')





# edit product;json file from here
def edit_products(request):
    json_path = Path(settings.BASE_DIR) / "shop/static/products.json"  # Path to the JSON file

    if request.method == "POST":
        try:
            # Parse raw JSON body
            body = json.loads(request.body.decode("utf-8"))
            updated_data = body.get("products_data", [])
            
            # Debugging
            print(f"Received data: {updated_data}")

            if not updated_data:
                return JsonResponse({"success": False, "message": "No data to update."})

            # Save updated data to JSON file
            with open(json_path, "w", encoding="utf-8") as jsonfile:
                json.dump(updated_data, jsonfile,ensure_ascii=False, indent=4)

            return JsonResponse({"success": True, "message": "Products updated successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # Load current JSON data
    with open(json_path, encoding="utf-8") as jsonfile:
            try:
                product_data = json.load(jsonfile)
                print(f"Loaded product data: {product_data}")  # Debugging print statement
            except json.JSONDecodeError as e:
                print(f"Error loading JSON: {e}")
                product_data = []  # Ensure product_data is a valid list if error occurs

    return render(request, "edit_products.html", {"products": product_data})



@login_required
def manage_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('manage_address')
    else:
        form = AddressForm()

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'manage_address.html', {'form': form, 'addresses': addresses})



from .models import Product
from django.db.models import Q



def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)

    if query:
        # Perform a case-insensitive search based on the product name
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    for product in products:
        # Dynamically set the image URL based on the product name (e.g., 'products/potato.jpg')
        product.image_url = f"images/products/{product.name.lower().replace(' ', '_')}.jpg"

    return render(request, 'product_search.html', {'products': products})









