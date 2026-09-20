import os

import cv2
import numpy as np

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from PIL import Image

from .models import WasteDetection, WasteCategory
from .ai_model import predict_waste
from .live_model import model


# =========================================================
# IMAGE UPLOAD + AI CLASSIFICATION
# =========================================================

@login_required
def upload_waste(request):

    if request.method == 'POST':

        image = request.FILES.get('uploaded_image')

        if not image:
            messages.error(
                request,
                'Please select a waste image.'
            )
            return redirect('upload_waste')

        image.name = os.path.basename(image.name)
        image.name = image.name.replace(" ", "_")

        allowed_extensions = [
            '.jpg',
            '.jpeg',
            '.png'
        ]

        file_extension = image.name.lower()

        if not any(
            file_extension.endswith(ext)
            for ext in allowed_extensions
        ):
            messages.error(
                request,
                'Invalid file extension. Only JPG, JPEG and PNG images are allowed.'
            )
            return redirect('upload_waste')

        allowed_types = [
            'image/jpeg',
            'image/png',
            'image/jpg'
        ]

        if image.content_type not in allowed_types:
            messages.error(
                request,
                'Only JPG, JPEG and PNG images are allowed.'
            )
            return redirect('upload_waste')

        try:

            img = Image.open(image)
            img.verify()

        except Exception:

            messages.error(
                request,
                'Invalid image file. Please upload a valid image.'
            )
            return redirect('upload_waste')

        max_size = 5 * 1024 * 1024

        if image.size > max_size:

            messages.error(
                request,
                'Image size must be less than 5 MB.'
            )
            return redirect('upload_waste')

        detection = WasteDetection.objects.create(
            user=request.user,
            uploaded_image=image
        )

        try:

            category_name, confidence = predict_waste(
                detection.uploaded_image.path
            )

            category = WasteCategory.objects.filter(
                name__iexact=category_name
            ).first()

            if not category:

                messages.error(
                    request,
                    'Predicted category was not found in database.'
                )

                return redirect('upload_waste')

            detection.predicted_category = category
            detection.confidence = confidence
            detection.disposal_recommendation = (
                category.disposal_recommendation
            )

            detection.save()

            messages.success(
                request,
                'Waste image analyzed successfully!'
            )

            return redirect(
                'upload_success',
                detection_id=detection.id
            )

        except Exception as e:

            messages.error(
                request,
                'Unable to analyze the image. Please try again.'
            )

            print(
                "AI Prediction Error:",
                e
            )

            return redirect('upload_waste')

    return render(
        request,
        'upload.html'
    )


# =========================================================
# UPLOAD RESULT PAGE
# =========================================================

@login_required
def upload_success(request, detection_id):

    detection = get_object_or_404(
        WasteDetection,
        id=detection_id,
        user=request.user
    )

    return render(
        request,
        'upload_success.html',
        {
            'detection': detection
        }
    )


# =========================================================
# DETECTION HISTORY
# =========================================================

@login_required
def detection_history(request):

    detections = (
        WasteDetection.objects
        .filter(user=request.user)
        .select_related('predicted_category')
        .order_by('-created_at')
    )

    return render(
        request,
        'history.html',
        {
            'detections': detections
        }
    )


# =========================================================
# YOLO LIVE DETECTION API
# =========================================================

@login_required
def live_detection_api(request):

    if request.method != 'POST':

        return JsonResponse(
            {
                'error': 'POST request required.'
            },
            status=405
        )

    image_file = request.FILES.get('frame')

    if not image_file:

        return JsonResponse(
            {
                'error': 'No frame received.'
            },
            status=400
        )

    try:

        image_bytes = image_file.read()

        np_array = np.frombuffer(
            image_bytes,
            np.uint8
        )

        frame = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:

            return JsonResponse(
                {
                    'error': 'Invalid image frame.'
                },
                status=400
            )

        results = model(
            frame,
            imgsz=320,
            conf=0.40,
            verbose=False
        )

        detections = []

        result = results[0]

        class_mapping = {

            "Paper": "Paper",

            "Plastic": "Plastic",

            "Glass": "Glass",

            "Metal": "Metal",

            "Organic": "Organic / Wet Waste",

            "Electronics": "E-Waste",

            "Miscellaneous": "General Waste"
        }

        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                raw_class_name = result.names[
                    class_id
                ]

                class_name = class_mapping.get(
                    raw_class_name,
                    raw_class_name
                )

                detections.append(
                    {
                        'class': class_name,

                        'confidence': round(
                            confidence * 100,
                            2
                        ),

                        'x1': x1,

                        'y1': y1,

                        'x2': x2,

                        'y2': y2
                    }
                )

        return JsonResponse(
            {
                'success': True,
                'detections': detections
            }
        )

    except Exception as e:

        print(
            "Live Detection Error:",
            e
        )

        return JsonResponse(
            {
                'success': False,
                'error': 'Unable to process frame.'
            },
            status=500
        )


# =========================================================
# CAPTURE & SAVE LIVE DETECTION
# =========================================================

@login_required
def capture_detection(request):

    if request.method != 'POST':

        return JsonResponse(
            {
                'success': False,
                'error': 'POST request required.'
            },
            status=405
        )

    image_file = request.FILES.get(
        'captured_image'
    )

    category_name = request.POST.get(
        'category'
    )

    confidence = request.POST.get(
        'confidence'
    )

    if not image_file:

        return JsonResponse(
            {
                'success': False,
                'error': 'No captured image received.'
            },
            status=400
        )

    if not category_name:

        return JsonResponse(
            {
                'success': False,
                'error': 'Waste category is missing.'
            },
            status=400
        )

    try:

        # -------------------------------------------------
        # Secure filename
        # -------------------------------------------------

        image_file.name = os.path.basename(
            image_file.name
        )

        image_file.name = image_file.name.replace(
            " ",
            "_"
        )

        # -------------------------------------------------
        # Validate file extension
        # -------------------------------------------------

        allowed_extensions = [
            '.jpg',
            '.jpeg',
            '.png'
        ]

        file_name = image_file.name.lower()

        if not any(
            file_name.endswith(ext)
            for ext in allowed_extensions
        ):

            return JsonResponse(
                {
                    'success': False,
                    'error': 'Only JPG, JPEG and PNG images are allowed.'
                },
                status=400
            )

        # -------------------------------------------------
        # Validate image
        # -------------------------------------------------

        try:

            img = Image.open(image_file)
            img.verify()

        except Exception:

            return JsonResponse(
                {
                    'success': False,
                    'error': 'Invalid image file.'
                },
                status=400
            )

        # -------------------------------------------------
        # Validate size
        # -------------------------------------------------

        max_size = 5 * 1024 * 1024

        if image_file.size > max_size:

            return JsonResponse(
                {
                    'success': False,
                    'error': 'Image size must be less than 5 MB.'
                },
                status=400
            )

        # -------------------------------------------------
        # Find category
        # -------------------------------------------------

        category_mapping = {

            "Paper": "paper",

            "Plastic": "plastic",

            "Glass": "glass",

            "Metal": "metal",

            "Organic / Wet Waste": "organic",

            "E-Waste": "e_waste",

            "General Waste": "general"
        }

        database_category_name = category_mapping.get(
            category_name,
            category_name
        )

        category = WasteCategory.objects.filter(
            name__iexact=database_category_name
        ).first()

        if not category:

            return JsonResponse(
                {
                    'success': False,
                    'error': 'Waste category not found in database.'
                },
                status=400
            )

        # -------------------------------------------------
        # Convert confidence
        # -------------------------------------------------

        try:

            confidence_value = float(
                confidence
            )

        except (TypeError, ValueError):

            confidence_value = 0.0

        # -------------------------------------------------
        # Create database record
        # -------------------------------------------------

        detection = WasteDetection.objects.create(

            user=request.user,

            uploaded_image=image_file,

            predicted_category=category,

            confidence=confidence_value,

            disposal_recommendation=(
                category.disposal_recommendation
            )
        )

        # -------------------------------------------------
        # Success response
        # -------------------------------------------------

        return JsonResponse(
            {
                'success': True,

                'message': 'Detection saved successfully!',

                'detection_id': detection.id,

                'category': category.name,

                'confidence': confidence_value
            }
        )

    except Exception as e:

        print(
            "Capture Save Error:",
            e
        )

        return JsonResponse(
            {
                'success': False,
                'error': 'Unable to save detection.'
            },
            status=500
        )


# =========================================================
# LIVE DETECTION PAGE
# =========================================================

@login_required
def live_detection_page(request):

    return render(
        request,
        'live_detection.html'
    )