from django.db import models
from django.contrib.auth.models import User


class WasteCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_recyclable = models.BooleanField(default=False)
    disposal_recommendation = models.TextField()

    def __str__(self):
        return self.name


class WasteDetection(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='waste_detections'
    )

    uploaded_image = models.ImageField(
        upload_to='waste_images/'
    )

    predicted_category = models.ForeignKey(
        WasteCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='detections'
    )

    confidence = models.FloatField(
        null=True,
        blank=True
    )

    disposal_recommendation = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.predicted_category}"