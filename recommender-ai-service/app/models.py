from django.db import models


class CustomerPreference(models.Model):
    """Store customer preferences for recommendations"""

    customer_id = models.IntegerField(unique=True)
    preferred_categories = models.JSONField(default=list)
    viewed_books = models.JSONField(default=list)
    purchased_books = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for Customer {self.customer_id}"
