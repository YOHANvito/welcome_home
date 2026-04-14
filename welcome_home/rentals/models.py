from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('bedspace', 'Bedspace'),
        ('house', 'House'),
    )

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    recommendation_score = models.IntegerField(default=0, blank=True, null=True)
    top_pick = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Lightweight local scoring only.
        No paid API call every time a landlord adds/edits a property.
        """
        score = 50

        title_text = (self.title or "").lower()
        location_text = (self.location or "").lower()
        amenities_text = (self.amenities or "").lower()
        description_text = (self.description or "").lower()

        sampaloc_keywords = ['sampaloc', 'ust', 'feu', 'ceu', 'review center', 'espana', 'dapitan', 'p. campa']
        amenity_keywords = ['wifi', 'bed', 'cabinet', 'study', 'aircon', 'security', 'cr', 'kitchen']

        for word in sampaloc_keywords:
            if word in location_text or word in description_text:
                score += 5

        for word in amenity_keywords:
            if word in amenities_text:
                score += 3

        if self.price:
            if self.price <= 5000:
                score += 20
            elif self.price <= 8000:
                score += 15
            elif self.price <= 12000:
                score += 10
            elif self.price <= 18000:
                score += 5

        if self.property_type in ['bedspace', 'apartment']:
            score += 5

        score = max(0, min(score, 100))
        self.recommendation_score = score
        self.top_pick = score >= 85

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='properties/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery image for {self.property.title}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('rescheduled', 'Rescheduled'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    move_in_date = models.DateField()
    message = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.renter} - {self.property} ({self.status})"


class Comment(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class SavedProperty(models.Model):
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_properties'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='saved_by_users'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('renter', 'property')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.renter.username} saved {self.property.title}"