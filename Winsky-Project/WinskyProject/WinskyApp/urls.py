from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('booking/',views.booking,name="booking"),
    path('package/',views.package,name="package"),
    path('login/', views.login_form, name='login'),
    path('accounts/login/', views.login_form, name='login_form'),
    path('register/',views.register_form,name="register"),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard,name="dashboard"),

#general contents

    path('site_primary_info/', views.site_primary_info, name='site_primary_info'),
    path('site_address_info/', views.site_address_info, name='site_address_info'),

    path('site_logo_favicon/', views.site_logo_favicon, name='site_logo_favicon'),
    path('contact_emails/', views.contact_emails, name='contact_emails'),

    path('update_contact_numbers/', views.update_contact_numbers, name='update_contact_numbers'),
    path('update_social_media_links/', views.update_social_media_links, name='update_social_media_links'),

    path('update_seotags/', views.update_seotags, name='update_seotags'),
    path('update_google_analytics/', views.update_google_analytics, name='update_google_analytics'),

    path('update_style/', views.update_style, name='update_style'),

# package

    
    path('addpackage/', views.addpackage, name='addpackage'),
    path('create_package/', views.create_package, name='create_package'),
    path('update_package/<slug:slug>/', views.update_package, name='update_package'),
    path('package_list/', views.package_list, name='package_list'),
    path('package/delete/<slug:slug>/', views.delete_package, name='delete_package'),
    path('create_package_list/', views.create_package_list, name='create_package_list'),
    path('update_create_package/<slug:slug>/', views.update_create_package, name='update_create_package'),
    path('package_blog/delete/<slug:slug>/', views.delete_create_package, name='delete_create_package'),
    path('package/toggle/<int:id>/', views.toggle_package, name='toggle_package'),
    path('tour_package/toggle/<int:id>/', views.tour_toggle_package, name='tour_toggle_package'),
    path('productdetails/<slug:slug>/', views.productdetails, name='productdetails'),
    path('contact/', views.contact, name='contact'),
    path('contact_us_list/', views.contact_us_list, name='contact_us_list'),


#reset password 

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/passwordresetform.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/passwordresetdone.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name='registration/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/passwordresetcomplete.html'), name='password_reset_complete'),
]