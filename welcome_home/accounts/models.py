from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('renter', 'Renter'),
        ('landlord', 'Landlord'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='renter')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


class EmailVerificationOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_verification_otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return (not self.is_used) and timezone.now() <= self.expires_at

    def __str__(self):
        return f"Email OTP for {self.user.username}"


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_reset_otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return (not self.is_used) and timezone.now() <= self.expires_at

    def __str__(self):
        return f"Password reset OTP for {self.user.username}"


class AdminOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return (not self.is_used) and timezone.now() <= self.expires_at

    def __str__(self):
        return f"Admin OTP for {self.user.username}"


class LoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    attempt_count = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    locked_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('username', 'ip_address')

    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until

    def __str__(self):
        return f"{self.username} - {self.ip_address}"


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('LOGOUT', 'Logout'),
        ('REGISTER', 'Register'),
        ('EMAIL_VERIFICATION_SENT', 'Email Verification Sent'),
        ('EMAIL_VERIFIED', 'Email Verified'),
        ('EMAIL_VERIFICATION_FAILED', 'Email Verification Failed'),
        ('PASSWORD_RESET_REQUESTED', 'Password Reset Requested'),
        ('PASSWORD_RESET_COMPLETED', 'Password Reset Completed'),
        ('PROFILE_UPDATED', 'Profile Updated'),
        ('ADMIN_MFA_SENT', 'Admin MFA Sent'),
        ('ADMIN_MFA_SUCCESS', 'Admin MFA Success'),
        ('PROPERTY_CREATED', 'Property Created'),
        ('PROPERTY_UPDATED', 'Property Updated'),
        ('BOOKING_CREATED', 'Booking Created'),
        ('BOOKING_ACCEPTED', 'Booking Accepted'),
        ('BOOKING_REJECTED', 'Booking Rejected'),
        ('BOOKING_RESCHEDULED', 'Booking Rescheduled'),
        ('BOOKING_DELETED', 'Booking Deleted'),
        ('PROPERTY_SAVED', 'Property Saved'),
        ('PROPERTY_UNSAVED', 'Property Unsaved'),
        ('COMMENT_CREATED', 'Comment Created'),
        ('UNAUTHORIZED_ACCESS', 'Unauthorized Access'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.created_at:%Y-%m-%d %H:%M:%S}"