from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rentals.models import Property

User = get_user_model()

class Command(BaseCommand):
    help = "Seed sample properties for Sampaloc, Manila"

    def handle(self, *args, **kwargs):
        landlord, created = User.objects.get_or_create(
            username='samplelandlord',
            defaults={
                'email': 'landlord@example.com',
                'role': 'landlord',
                'phone': '09123456789'
            }
        )

        if created:
            landlord.set_password('password123')
            landlord.save()

        sample_data = [
            {
                "title": "Cozy Bedspace near UST",
                "property_type": "bedspace",
                "description": "Affordable and student-friendly bedspace near the University of Santo Tomas.",
                "price": 4500,
                "location": "Near UST, España Blvd., Sampaloc, Manila (District 4)",
                "latitude": 14.609000,
                "longitude": 120.989700,
                "amenities": "WiFi, fan, study area, shared kitchen",
                "tags": ["bedspace", "near school", "wifi"]
            },
            {
                "title": "Student Condo near NU Manila",
                "property_type": "condo",
                "description": "Clean and secure condo unit ideal for students and young professionals.",
                "price": 12000,
                "location": "Near NU Manila, M.F. Jhocson St., Sampaloc, Manila (District 4)",
                "latitude": 14.605600,
                "longitude": 120.994000,
                "amenities": "WiFi, aircon, furnished, security",
                "tags": ["condo", "furnished", "wifi"]
            },
            {
                "title": "Apartment near FEU",
                "property_type": "apartment",
                "description": "Comfortable apartment near Far Eastern University and other U-Belt schools.",
                "price": 8500,
                "location": "Near FEU, Nicanor Reyes St., Sampaloc, Manila (District 4)",
                "latitude": 14.604200,
                "longitude": 120.987600,
                "amenities": "Own CR, WiFi, sink, accessible transport",
                "tags": ["apartment", "near school", "student friendly"]
            },
            {
                "title": "Furnished Room near P. Campa",
                "property_type": "apartment",
                "description": "Simple furnished room in a convenient student area in Sampaloc.",
                "price": 7000,
                "location": "Near P. Campa St., Sampaloc, Manila (District 4)",
                "latitude": 14.607500,
                "longitude": 120.990500,
                "amenities": "Bed, cabinet, WiFi, water included",
                "tags": ["furnished", "wifi", "near school"]
            }
        ]

        for item in sample_data:
            property_obj, created = Property.objects.get_or_create(
                title=item["title"],
                defaults={
                    "landlord": landlord,
                    "property_type": item["property_type"],
                    "description": item["description"],
                    "price": item["price"],
                    "location": item["location"],
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "amenities": item["amenities"],
                    "is_available": True,
                }
            )
            property_obj.tags.set(item["tags"])

        self.stdout.write(self.style.SUCCESS("Sample Sampaloc properties seeded successfully."))