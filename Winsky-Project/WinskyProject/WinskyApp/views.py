from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, auth
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GeneralContent
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404
import os
from django.core.paginator import Paginator
from .models import GeneralContent
from .models import Package
from django.db import IntegrityError
from PIL import Image as PILImage
import os

def compress_and_save_image(image, target_size_kb=1000):
    img = PILImage.open(image.path)

    # Convert the image to RGB mode (JPEG format)
    img = img.convert("RGB")

    # Determine the initial quality level
    quality = 85

    # Loop while the image size is larger than the target size
    while os.path.getsize(image.path) > target_size_kb * 1024 and quality >= 5:
        # Save the image with the current quality level
        img.save(image.path, format='JPEG', quality=quality, optimize=True)
        
        # Decrease the quality level for the next iteration
        quality -= 5
from PIL import Image as PILImage

def resize_and_compress_image(image, target_width=1500, target_height=1000):
   
    
    img = PILImage.open(image)
    img = img.resize((target_width, target_height), PILImage.BILINEAR)  # Using BILINEAR resampling
    

    
    img.save(image.path, format='JPEG', quality=85)  # Save as JPEG with quality 85


def login_form(request):
   
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            remember_me = request.POST.get('remember_me', False)

            user = auth.authenticate(
                request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                  
                    request.session.set_expiry(0)

                return redirect('dashboard')
            else:
                error_message = 'Invalid username/password'
                return render(request, 'login.html', {'error_message': error_message})
        else:

            return render(request, 'login.html')
    except Exception as e:

        error_message = 'An error occurred: ' + str(e)
        return render(request, 'login.html', {'error_message': error_message})


def register_form(request):
    if request.method == 'POST':
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            password = request.POST['password']
            confirmpassword = request.POST['Confirmpassword']
            email = request.POST['email']

            if password == confirmpassword:
                if User.objects.filter(username=username).exists():
                    error_message = 'Username is already taken. Please try again.'
                    return render(request, 'register.html', {'error_message': error_message})
                elif User.objects.filter(email=email).exists():
                    error_message = "This email has already been registered. Please try again."
                    return render(request, 'register.html', {'error_message': error_message})
                else:
                    tab = User.objects.create_user(
                        username=username, first_name=firstname, last_name=lastname, password=password, email=email)
                    tab.save()
                    return redirect('login_form')
            else:
                error_message = "Password verification failed. Please try again."
                return render(request, 'register.html', {'error_message': error_message})
        except KeyError as e:
            error_message = f"Missing required field: {e}"
            return render(request, 'register.html', {'error_message': error_message})
    else:

        return render(request, 'register.html')


def logout(request):
    try:
        auth.logout(request)
        return redirect(login_form)
    except Exception as e:

        error_message = 'An error occurred: ' + str(e)
        return render(request, 'logout.html', {'error_message': error_message})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/passwordresetconfirm.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.is_valid():
            messages.error(
                self.request, 'Password reset failed. Please try again.')
            return render(self.request, self.template_name, {'form': form})

        # Render the 'confirmpassword.html' template
        return render(self.request, 'registration/passwordresetcomplete.html')

@login_required
def dashboard(request):
    obj=GeneralContent.objects.all()
    total_count = AddPackage.objects.count()
    package_count = Package.objects.count()
    contact = ContactMessage.objects.count()
    return render(request,'dashboard.html',{'obj':obj,'total_count':total_count,'package_count':package_count,'contact':contact})



def site_primary_info(request):
    obj = GeneralContent.objects.all()

    try:
        content = GeneralContent.objects.get(pk=1)
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            content = GeneralContent.objects.get(
                pk=1) if content else GeneralContent()
            content.sitename = request.POST['sitename']
            content.sitedescription = request.POST['sitedescription']
            content.save()

            messages.success(
                request, 'The modifications have been successfully saved.')
            return redirect(site_primary_info)
        except Exception as e:

            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'primarylogo.html', {'general_content': content, 'obj': obj})


def site_address_info(request):
    obj = GeneralContent.objects.all()
    try:
        content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            country = request.POST.get('country')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')

            if address1 or country or city: 
                content = GeneralContent.objects.first() if content else GeneralContent()
                content.address1 = address1
                content.address2 = address2
                content.country = country
                content.city = city
                content.zipcode = zipcode
                content.save()
                messages.success(
                    request, 'The modifications have been successfully saved.')
                return redirect(site_address_info)
        except Exception as e:
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'addressinfo.html', {'general_content': content, 'obj': obj})


def site_logo_favicon(request):
    obj = GeneralContent.objects.all()
    try:
        content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            content.sitelogo = request.FILES.get(
                'sitelogo') or content.sitelogo
            content.browsersitelogo = request.FILES.get(
                'browsersitelogo') or content.browsersitelogo
            content.save()
            messages.success(
                request, 'The modifications have been successfully saved.')
            return redirect('site_logo_favicon')
        except Exception as e:

            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'primarylogo.html', {'general_content': content, 'obj': obj})


def contact_emails(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            primary_email = request.POST.get('primaryemail')
            secondary_email = request.POST.get('secondaryemail')
            replaytoemail = request.POST.get('replaytoemail')

            general_content.primaryemail = primary_email
            general_content.secondaryemail = secondary_email
            general_content.replaytoemail = replaytoemail
            general_content.save()
            messages.success(
                request, "The modifications have been successfully saved.")
            return redirect(contact_emails)
        except Exception as e:

            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'emailcontact.html', {'general_content': general_content, 'obj': obj})


def update_contact_numbers(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            primary_contact_number = request.POST.get('primary_contact_number')
            secondary_contact_number = request.POST.get(
                'secondary_contact_number')
            tertiary_contact_number = request.POST.get(
                'tertiary_contact_number')

            # Update the general content object
            general_content.primarycontactnumber = primary_contact_number
            general_content.secondarycontactnumber = secondary_contact_number
            general_content.tertiarycontactnumber = tertiary_contact_number
            general_content.save()
            messages.success(
                request, 'The changes have been saved successfully')
            return redirect(update_contact_numbers)
        except Exception as e:
          
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'emailcontact.html', {'general_content': general_content, 'obj': obj})


def update_social_media_links(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None
    except Exception as e:
       
        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            facebookurl = request.POST.get('facebookurl')
            twitterurl = request.POST.get('twitterurl')
            instagramurl = request.POST.get('instagramurl')
            skypeurl = request.POST.get('skypeurl')
            linkedinurl = request.POST.get('linkedinurl')

            general_content.facebookurl = facebookurl
            general_content.twitterurl = twitterurl
            general_content.instagramurl = instagramurl
            general_content.skypeurl = skypeurl
            general_content.linkedinurl = linkedinurl

            general_content.save()
            messages.success(
                request, 'The modifications have been successfully saved.')
            return redirect(update_social_media_links)
        except Exception as e:
           
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'mediatags.html', {'general_content': general_content, 'obj': obj})


def update_seotags(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = get_object_or_404(GeneralContent, pk=1)
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        metakeywords = request.POST.get('metakeywords')
        metadescription = request.POST.get('metadescription')

        general_content.metakeywords = metakeywords
        general_content.metadescription = metadescription
        general_content.save()
        messages.success(
            request, "The modifications have been successfully saved.")
     
        return redirect('update_seotags')

    return render(request, 'mediatags.html', {'general_content': general_content, 'obj': obj})


def update_google_analytics(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        googleanalyticscode = request.POST.get('googleanalyticscode')

        general_content.googleanalyticscode = googleanalyticscode
        general_content.save()
        messages.success(
            request, "The modifications have been successfully saved.")
       
        return redirect('update_google_analytics')

    return render(request, 'googleanalytics_css.html', {'general_content': general_content, 'obj': obj})


def update_style(request):
   
    obj = GeneralContent.objects.first()  
    
    css_content = obj.cssinput if obj else ""
   
    js_content = obj.jsinput if obj else ""

 
    css_file_path = os.path.join(
        os.path.dirname(__file__),
        'static',
        'assets',
        'css',
        'custom.css'
    )
    js_file_path = os.path.join(
        os.path.dirname(__file__),
        'static',
        'assets',
        'js',
        'custom.js'
    )

  
    with open(css_file_path, 'w') as css_file:
        css_file.write(css_content)


    with open(js_file_path, 'w') as js_file:
        js_file.write(js_content)

    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        cssinput = request.POST.get('cssinput')
        jsinput = request.POST.get('jsinput')

        general_content.cssinput = cssinput
        general_content.jsinput = jsinput
        general_content.save()

        messages.success(
            request, "The modifications have been successfully saved.")
  
        return redirect('update_style')

    return render(request, 'googleanalytics_css.html', {'general_content': general_content, 'obj': obj})

def index(request):
    obj = GeneralContent.objects.all()
    selected_addpackages = AddPackage.objects.filter(is_selected=True).order_by('-id')
    active_packages = Package.objects.filter(is_active=True).order_by('-id')
    addpackages = AddPackage.objects.select_related('package').filter(package__in=active_packages, is_active=True)
    return render(request, 'index.html', {'obj': obj, 'selected_addpackages': selected_addpackages,'active_packages': active_packages, 'addpackages': addpackages})

def about(request):
    obj= GeneralContent.objects.all()
    return render(request,'about.html',{'obj':obj})


def blog(request):
    obj= GeneralContent.objects.all()
    return render(request,'blog.html',{'obj':obj})


def booking(request):
    obj= GeneralContent.objects.all()
    return render(request,'booking.html',{'obj':obj})
from django.shortcuts import render
from .models import Package, AddPackage

def package(request):
    obj = GeneralContent.objects.all()  # You didn't define GeneralContent in the provided code
    packages = Package.objects.all()
    addpackages = AddPackage.objects.select_related('package').order_by('-id')


    return render(request, 'package.html', {'obj': obj, 'packages': packages, 'addpackages': addpackages})


def addpackage(request):
    if request.method == 'POST':
        name= request.POST['title']
        description = request.POST['description']

        try:
            packageobj = Package( name=name, description=description)
            packageobj.save()
            messages.success(
                        request, 'You have completed your task successfully')
            return redirect('addpackage')
        except IntegrityError:
                    error_message = 'An integrity error occurred while saving your content.'
                    messages.error(request, error_message)
                    return redirect('addpackage')
        except Exception as e:
                    error_message = 'An internal server error occurred.'
                    messages.error(request, error_message)
                    return redirect('addpackage')
    packages=Package.objects.all()
    obj=GeneralContent.objects.all()

    return render(request,'addpackage.html',{'packages':packages,'obj':obj})
from django.conf import settings
import os
from django.shortcuts import redirect, render
from django.contrib import messages

def create_package(request):
    if request.method == 'POST':
        try:
            package_id = request.POST.get('package')
            rate = request.POST.get('rate', 0)
            days = request.POST.get('days', 0)
            nights = request.POST.get('nights', 0)
            people = request.POST.get('people', 0)
            country = request.POST.get('country', '')
            image = request.FILES.get('image')
            image_caption = request.POST.get('image_caption', '')
            image_description = request.POST.get('image_description', '')
            image_files = request.FILES.getlist('image1[]')
            famous_place = request.POST.get('famous_place', '')
            city_visit = request.POST.get('city_visit', '')
            rooms = request.POST.get('rooms', '')
            food = request.POST.get('food', '')
            rating = request.POST.get('rating', 1)

            new_package = AddPackage(
                package_id=package_id,
                rate=rate,
                days=days,
                nights=nights,
                famous_place=famous_place,
                city_visit=city_visit,
                rooms=rooms,
                food=food,
                people=people,
                country=country,
                image=image,
                image_caption=image_caption,
                image_description=image_description,
                rating=rating
            )
            new_package.save()

            if image:
                print(f"Main image path: {image.name}")
            for image_file in image_files:
                print(f"Additional image file: {image_file.name}")

            # Ensure the media directory exists
            media_dir = os.path.join(settings.MEDIA_ROOT, 'Package_Images')
            if not os.path.exists(media_dir):
                print(f"Creating directory: {media_dir}")
                os.makedirs(media_dir)

            # Save the main image
            if image:
                image_instance = Image(file=image)
                image_instance.save()
                new_package.image = image_instance

            # Save additional images
            for image_file in image_files:
                image_instance = Image(file=image_file)
                image_instance.save()
                new_package.image1.add(image_instance)

            new_package.save()

            messages.success(request, 'Package created successfully!')

            return redirect(create_package)

        except Exception as e:
            #messages.error(request, f"An error occurred: {str(e)}")
            return redirect(create_package)

    obj = GeneralContent.objects.all()
    packages = Package.objects.all()
    return render(request, 'packageblogcontent.html', {'obj': obj, 'packages': packages})


def update_package(request, slug):
    try:
        package = Package.objects.get(slug=slug)
    except Package.DoesNotExist:
        messages.error(request, 'Package not found.')
        return redirect('update_package')

    if request.method == 'POST':
        name = request.POST['title']
        description = request.POST['description']

        try:
            package.name = name
            package.description = description
            package.save()
            messages.success(request, 'Package updated successfully.')
            return redirect('update_package',slug=package.slug)
        except IntegrityError:
            error_message = 'An integrity error occurred while saving your content.'
            messages.error(request, error_message)
            return redirect('update_package',slug=package.slug)
        except Exception as e:
            error_message = 'An internal server error occurred.'
            messages.error(request, error_message)
            return redirect('update_package',slug=package.slug)

   
    obj = GeneralContent.objects.all()
    

    return render(request, 'updatepackage.html', {'package': package, 'obj': obj})

def package_list(request):
    obj = GeneralContent.objects.all()
    package_list = Package.objects.order_by('-id')
    paginator = Paginator(package_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'packagelist.html', {'page_obj': page_obj, 'obj': obj})


def delete_package(request, slug):
    try:
        package = Package.objects.get(slug=slug)
        package.delete()

    except Package.DoesNotExist:
        messages.error(request, 'The package you requested does not exist')
    return redirect('package_list')
from django.http import JsonResponse

def create_package_list(request):
    obj = GeneralContent.objects.all()
    addpackage = AddPackage.objects.select_related('package').order_by('-id')
    paginator = Paginator(addpackage, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        is_selected = request.POST.get('is_selected', False)  # Ensure that the parameter name matches the one in the template
        package = get_object_or_404(AddPackage, pk=package_id)
        package.is_selected = bool(is_selected)
        package.save()
        return JsonResponse({'status': 'success', 'message': 'is_selected updated successfully'})

    return render(request, 'packagebloglist.html', {'page_obj': page_obj, 'obj': obj})

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import AddPackage, Image

def update_create_package(request, slug):
  obj = GeneralContent.objects.all()
  packages = Package.objects.all()
  try:
        package = AddPackage.objects.get(slug=slug)
  except AddPackage.DoesNotExist:
        messages.error(request, 'Package not found.')
        return redirect('update_package', slug=slug)  # Adjust the URL name as needed

  if request.method == 'POST':
        try:
            package_id = request.POST.get('package')
            rate = request.POST.get('rate', 0)
            days = request.POST.get('days', 0)
            nights = request.POST.get('nights', 0)
            people = request.POST.get('people', 0)
            country = request.POST.get('country', '')
            image = request.FILES.get('image')
            image_caption = request.POST.get('image_caption', '')
            image_description = request.POST.get('image_description', '')
            image_files = request.FILES.getlist('image1[]')
            famous_place = request.POST.get('famous_place', '')
            city_visit = request.POST.get('city_visit', '')
            rooms = request.POST.get('rooms', '')
            food = request.POST.get('food', '')
            rating = request.POST.get('rating', 1)

            package.package_id = package_id
            package.rate = rate
            package.days = days
            package.nights = nights
            package.famous_place = famous_place
            package.city_visit = city_visit
            package.rooms = rooms
            package.food = food
            package.people = people
            package.country = country

            if image:
                package.image = image

            package.image_caption = image_caption
            package.image_description = image_description
            package.rating = rating

            package.save()

            # Clear and update image1 field if new images are provided
            if image_files:
                # Clear existing images
                package.image1.clear()
                for image_file in image_files:
                    image = Image(file=image_file)
                    image.save()
                    package.image1.add(image)

            resize_and_compress_image(package.image)
            messages.success(request, 'Package updated successfully!')

            return redirect('update_create_package', slug=package.slug)  # Adjust the URL name as needed

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
  addpackage = AddPackage.objects.all()
  image_urls = [image.file.url for product_obj in addpackage for image in product_obj.image1.all()]

  return render(request, 'updatepackageblog.html', {'obj': obj, 'package': package,'image_urls':image_urls, 'packages': packages})

 
def delete_create_package(request, slug):
    try:
        package = AddPackage.objects.get(slug=slug)
        package.delete()

    except Package.DoesNotExist:
        messages.error(request, 'The package you requested does not exist')
    return redirect('create_package_list')

from django.shortcuts import get_object_or_404, redirect
from .models import AddPackage  # Import your package model here

from django.shortcuts import get_object_or_404, redirect

def toggle_package(request, id):
    package = get_object_or_404(AddPackage, id=id)
    package.is_selected = not package.is_selected
    package.save()
    return redirect('create_package_list')  # Make sure 'create_package_list' is the correct URL name

def tour_toggle_package(request, id):
    tour_package = get_object_or_404(Package, id=id)
    tour_package.is_active = not tour_package.is_active
    tour_package.save()
    return redirect('package_list')
    
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError
from django.db.models import Q
from .models import GeneralContent, AddPackage  # Import your models

def productdetails(request, slug):
    try:
        obj = GeneralContent.objects.all()
        current_package = get_object_or_404(AddPackage, slug=slug)

        similar_packages = AddPackage.objects.filter(
            days=current_package.days,
            nights=current_package.nights,
            rate=current_package.rate
        ).exclude(slug=slug)

        return render(request, 'package-details.html', {'obj': obj, 'current_package': current_package, 'similar_packages': similar_packages})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")
from .models import ContactMessage

def contains_letter(s):
    return any(c.isalpha() for c in s)
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    obj = GeneralContent.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('comments')

        # Perform additional validation on the first name (isalpha())
        if not first_name.isalpha():
            messages.error(request, 'Please kindly provide a valid first name. Thank you.')
            return redirect('contact')

        if not last_name.isalpha():
            messages.error(request, 'Please kindly provide a valid first name. Thank you.')
            return redirect('contact')
        # Perform additional validation on the message (contains_letter())
        if not any(c.isalpha() for c in message):
            messages.error(request, 'Please ensure that you have mentioned your message. Thank you.')
            return redirect('contact')

        # Validate phone number contains only digits
        if not phone.isdigit():
            messages.error(request, 'Kindly ensure accurate and proper entry of your phone number. Thank you.')
            return redirect('contact')

        # Validate phone number length
        if len(phone) > 15:
            messages.error(request, 'Kindly ensure accurate and proper entry of your phone number. Thank you.')
            return redirect('contact')

        # Save the data to the database
        contact_message = ContactMessage(
            firstname=first_name,
            lastname=last_name,
            email=email,
            phone=phone,
            message=message,
        )
        contact_message.save()

        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')  # Redirect to a success page

    return render(request, 'contact.html',{'obj':obj})

def contact_us_list(request):
    
    obj = GeneralContent.objects.all()
    contact = ContactMessage.objects.order_by('-id')
    paginator = Paginator(contact, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contactenquirytable.html', {'page_obj': page_obj,'obj':obj})
