from django import forms
from django.conf import settings
from PIL import Image

from .models import Property, Booking, Comment


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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned_files = []
        for uploaded_file in data:
            cleaned_files.append(validate_safe_image(uploaded_file))
        return cleaned_files


class PropertyForm(forms.ModelForm):
    gallery_images = MultipleFileField(required=False)

    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'description', 'price', 'location',
            'latitude', 'longitude', 'amenities', 'image', 'is_available', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter property title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter property description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter rental price'}),
            'location': forms.TextInput(attrs={'placeholder': 'Example: Near UST, Sampaloc, Manila (District 4)'}),
            'latitude': forms.NumberInput(attrs={'placeholder': 'Example: 14.609000'}),
            'longitude': forms.NumberInput(attrs={'placeholder': 'Example: 120.989700'}),
            'amenities': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Example: WiFi, bed, cabinet, study area'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return validate_safe_image(image)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['move_in_date', 'message']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message to landlord'}),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        return message.strip()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content