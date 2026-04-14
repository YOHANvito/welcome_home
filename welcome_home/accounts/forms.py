from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from PIL import Image

from .models import CustomUser


ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


def validate_safe_image(uploaded_file):
    if not uploaded_file:
        return uploaded_file

    max_size = getattr(settings, 'MAX_UPLOAD_SIZE_MB', 5) * 1024 * 1024
    if uploaded_file.size > max_size:
        raise forms.ValidationError(
            f"Image must be smaller than {getattr(settings, 'MAX_UPLOAD_SIZE_MB', 5)}MB."
        )

    filename = uploaded_file.name.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
        raise forms.ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")

    try:
        image = Image.open(uploaded_file)
        image.verify()
    except Exception:
        raise forms.ValidationError("Uploaded file is not a valid image.")

    uploaded_file.seek(0)
    return uploaded_file


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'role': forms.Select(),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if email and qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        return validate_safe_image(image)


class AdminOTPForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit verification code',
            'autocomplete': 'one-time-code'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code.isdigit():
            raise forms.ValidationError("Verification code must contain numbers only.")
        return code


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email'})
    )


class PasswordResetCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit reset code',
            'autocomplete': 'one-time-code'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code.isdigit():
            raise forms.ValidationError("Verification code must contain numbers only.")
        return code


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'})
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit email verification code',
            'autocomplete': 'one-time-code'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code.isdigit():
            raise forms.ValidationError("Verification code must contain numbers only.")
        return code