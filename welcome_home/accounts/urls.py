from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('verify-admin-otp/', views.verify_admin_otp_view, name='verify_admin_otp'),

    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_otp_view, name='resend_verification'),

    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/verify/', views.password_reset_verify_view, name='password_reset_verify'),
    path('password-reset/resend/', views.resend_password_reset_otp_view, name='resend_password_reset'),
    path('password-reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),

    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('dashboard-admin/', views.admin_dashboard_view, name='dashboard_admin'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-properties/', views.admin_properties, name='admin_properties'),
    path('admin-bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('admin-settings/', views.admin_settings, name='admin_settings'),

    path('dashboard-landlord/', views.landlord_dashboard, name='dashboard_landlord'),
    path('landlord-properties/', views.landlord_properties_view, name='landlord_properties'),
    path('landlord-tenants/', views.landlord_tenants, name='landlord_tenants'),
    path('landlord-messages/', views.landlord_messages, name='landlord_messages'),
    path('landlord-settings/', views.landlord_settings, name='landlord_settings'),

    path('dashboard-client/', views.client_dashboard, name='dashboard_client'),
    path('client-saved/', views.client_saved, name='client_saved'),
    path('client-messages/', views.client_messages, name='client_messages'),
    path('client-settings/', views.client_settings, name='client_settings'),

    path('renter-bookings/', views.renter_bookings_view, name='renter_bookings'),

    path('booking/<int:pk>/accept/', views.booking_accept, name='booking_accept'),
    path('booking/<int:pk>/reject/', views.booking_reject, name='booking_reject'),
    path('booking/<int:pk>/reschedule/', views.booking_reschedule, name='booking_reschedule'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
]