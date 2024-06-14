
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image as PILImage
import shutil
import io
import os
from django.core.files.base import ContentFile

def upload_to(instance, filename):
    return f'Site_logo/{filename}'
    
class GeneralContent(models.Model):
    sitename = models.CharField(max_length=255, default="")
    slug = models.SlugField(max_length=255, unique=True)
    sitedescription = models.TextField()
    address1 = models.CharField(max_length=255, default=" ")
    address2 = models.CharField(max_length=255, default=" ")
    country = models.CharField(max_length=100, default=" ")
    city = models.CharField(max_length=255, default=" ")
    zipcode = models.CharField(max_length=20, default=" ")
    sitelogo = models.ImageField(upload_to='Site_logo/', blank=True)
    browsersitelogo = models.ImageField(upload_to='Browser_tag_logo/',blank=True)
    primaryemail = models.EmailField(default=" ")
    secondaryemail = models.EmailField(default=" ")
    replaytoemail = models.EmailField(default=" ")
    primarycontactnumber = models.CharField(max_length=20, default=" ")
    secondarycontactnumber = models.CharField(max_length=20, default=" ")
    tertiarycontactnumber = models.CharField(max_length=20, default=" ")
    facebookurl = models.CharField(max_length=255, default=" ")
    twitterurl = models.CharField(max_length=255, default=" ")
    instagramurl = models.CharField(max_length=255, default=" ")
    skypeurl = models.CharField(max_length=255, default=" ")
    linkedinurl = models.CharField(max_length=255, default=" ")
    metakeywords = models.CharField(max_length=255, default=" ")
    metadescription = models.CharField(max_length=50000, default=" ")
    googleanalyticscode = models.CharField(max_length=50000, default=" ")
    cssinput = models.CharField(max_length=255, default=" ")
    jsinput = models.CharField(max_length=255, default=" ")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

   
   
    def save(self, *args, **kwargs):
        if self.browsersitelogo:
            img = PILImage.open(self.browsersitelogo)
            img = img.convert("RGBA")

            # Resize the image to a smaller size (32x32) before processing
            img = img.resize((32, 32), PILImage.BILINEAR)

            ico_data = io.BytesIO()
            img.save(ico_data, format="ICO")

            # Save the ICO data as a ContentFile to the browsersitelogo field
            self.browsersitelogo.save('favicon.ico', ContentFile(ico_data.getvalue()), save=False)

        if self.sitelogo:
            original_sitelogo = None
            
            try:
                # Check if the instance is being updated and get the original sitelogo
                original_instance = GeneralContent.objects.get(pk=self.pk)
                original_sitelogo = original_instance.sitelogo
            except GeneralContent.DoesNotExist:
                pass
        
        # If the sitelogo is new or different, rename it
            if original_sitelogo != self.sitelogo:
                # Delete the existing logo if it exists
                if original_sitelogo:
                    original_sitelogo.storage.delete(original_sitelogo.name)

                # Get the original filename and extension
                original_filename, extension = self.sitelogo.name.rsplit('.', 1)

                # Rename the image to 'logo.extension'
                new_filename = 'logo.' + extension
                self.sitelogo.name = 'Site_logo/' + new_filename


        super().save(*args, **kwargs)

    def __str__(self):
        return self.sitename



class Package(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Package.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AddPackage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_selected = models.BooleanField(default=False)
    rate = models.CharField(max_length=10, default='0')
    days = models.IntegerField(default=0)
    nights = models.IntegerField(default=0)
    people = models.IntegerField(default=0)
    country = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to='Package_Images/', blank=True)
    image1 = models.ManyToManyField('Image', related_name='package_gallery')
    condition1 = models.CharField(max_length=1000, default="")
    condition2 = models.CharField(max_length=1000, default="")
    condition3 = models.CharField(max_length=1000, default="")
    condition4 = models.CharField(max_length=1000, default="")
    condition5 = models.CharField(max_length=1000, default="")
    famous_place =  models.CharField(max_length=1000, default="")
    city_visit = models.CharField(max_length=1000, default="")
    rooms = models.CharField(max_length=1000, default="")
    food = models.CharField(max_length=1000, default="")
    image_caption = models.CharField(max_length=1000, default="")
    image_description = models.CharField(max_length=1000, default="")

    rating = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.image_caption)
            slug = base_slug
            counter = 1
            while AddPackage.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.image_caption

class Image(models.Model):
    file = models.ImageField(upload_to='Package_Images/')
    def __str__(self):
        return str(self.file)

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    add_package = models.ManyToManyField(AddPackage)
    slug = models.SlugField(max_length=255, unique=True)

    def add_to_wishlist(self, packages):
        self.add_package.add(packages)

    def remove_from_wishlist(self, packages):
        self.add_package.remove(packages)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.user.username + "'s Wishlist")
            slug = base_slug
            counter = 1
            while Wishlist.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class TravelPackage(models.Model):
    from_destination = models.CharField(max_length=100)  # You can adjust the max_length as needed
    to_destination = models.CharField(max_length=100)
    check_date = models.DateField()
    duration = models.CharField(max_length=20)  # You can adjust the max_length as needed

    def __str__(self):
        return f"{self.from_destination} to {self.to_destination}"

    class Meta:
        verbose_name_plural = "Travel Packages"


class ContactMessage(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.email}"