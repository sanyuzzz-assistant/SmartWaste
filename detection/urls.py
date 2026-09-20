from django.urls import path
from . import views


urlpatterns = [

    path(
        'upload/',
        views.upload_waste,
        name='upload_waste'
    ),

    path(
        'upload/success/<int:detection_id>/',
        views.upload_success,
        name='upload_success'
    ),

    path(
        'history/',
        views.detection_history,
        name='detection_history'
    ),

    path(
        'live-detection/api/',
        views.live_detection_api,
        name='live_detection_api'
    ),

    path(
        'live-detection/capture/',
        views.capture_detection,
        name='capture_detection'
    ),

    path(
        'live-detection/',
        views.live_detection_page,
        name='live_detection'
    ),
]