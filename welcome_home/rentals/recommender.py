from .models import Property


def get_recommended_properties(user):
    available_properties = Property.objects.filter(is_available=True).order_by('-created_at')

    if not available_properties.exists():
        return []

    recommended = []

    booked_property_ids = []
    saved_property_ids = []
    preferred_types = []
    preferred_locations = []
    preferred_tags = set()

    if user.is_authenticated:
        user_bookings = user.bookings.select_related('property').all()
        user_saved = user.saved_properties.select_related('property').all()

        booked_property_ids = [b.property_id for b in user_bookings if b.property_id]
        saved_property_ids = [s.property_id for s in user_saved if s.property_id]

        related_properties = [
            b.property for b in user_bookings if b.property
        ] + [
            s.property for s in user_saved if s.property
        ]

        for prop in related_properties:
            if prop.property_type:
                preferred_types.append(prop.property_type)

            if prop.location:
                preferred_locations.append(prop.location.lower())

            for tag in prop.tags.all():
                preferred_tags.add(tag.name.lower())

    for item in available_properties:
        score = 0
        reasons = []

        if user.is_authenticated:
            if item.id in saved_property_ids:
                score += 4
                reasons.append("Based on your saved properties")

            if item.property_type in preferred_types:
                score += 3
                reasons.append("Matches your preferred property type")

            item_tags = {tag.name.lower() for tag in item.tags.all()}
            common_tags = preferred_tags.intersection(item_tags)
            if common_tags:
                score += 2
                reasons.append("Matches your preferred tags")

            if item.location:
                item_location = item.location.lower()
                if any(loc in item_location or item_location in loc for loc in preferred_locations):
                    score += 3
                    reasons.append("Similar to your preferred location")

        else:
            if item.location and 'sampaloc' in item.location.lower():
                score += 3
                reasons.append("Popular in Sampaloc area")

        try:
            price_value = float(item.price)
            if price_value <= 10000:
                score += 2
                reasons.append("Affordable option")
            elif price_value <= 18000:
                score += 1
                reasons.append("Mid-range option")
        except Exception:
            pass

        if item.amenities:
            amenities_text = item.amenities.lower()
            useful_keywords = ['wifi', 'aircon', 'security', 'laundry', 'furnished', 'study', 'parking']
            matched = [word for word in useful_keywords if word in amenities_text]
            if matched:
                score += min(2, len(matched))
                reasons.append("Useful amenities included")

        item.recommendation_score = score
        item.recommendation_reason = ", ".join(reasons) if reasons else "Suggested for general browsing"

        if score >= 7:
            item.recommendation_level = "High Match"
        elif score >= 4:
            item.recommendation_level = "Medium Match"
        else:
            item.recommendation_level = "Low Match"

        recommended.append(item)

    recommended = sorted(
        recommended,
        key=lambda x: (-x.recommendation_score, -x.created_at.timestamp())
    )[:6]

    if recommended:
        recommended[0].top_pick = True

    return recommended