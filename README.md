# SmartWaste – Garbage Detection and Recognition System

SmartWaste is an AI-powered web application developed to detect and classify different types of waste using image classification and real-time object detection.

The system allows users to upload waste images for classification and also provides real-time waste detection through a webcam using YOLO.

---

## 🚀 Features

- User Registration and Login
- User Dashboard
- Waste Image Upload
- AI-based Waste Classification using CNN
- Real-Time Waste Detection using YOLO
- Webcam-based Detection
- Capture Detection Results
- Detection History
- User Profile and Statistics
- Admin Dashboard
- Django Admin Panel
- Waste Category Management
- Recyclability Information
- Disposal Recommendations
- MySQL Database Integration

---

## ♻️ Waste Categories

SmartWaste supports the following waste categories:

1. Plastic
2. Paper
3. Glass
4. Metal
5. Organic / Wet Waste
6. E-Waste
7. General Waste

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Django

### Database
- MySQL

### Machine Learning
- TensorFlow
- Keras
- Convolutional Neural Network (CNN)

### Computer Vision
- OpenCV
- Pillow

### Object Detection
- Ultralytics YOLO
- YOLO11n

---

## 🧠 AI/ML Approach

SmartWaste uses two AI approaches:

### 1. CNN Image Classification

The CNN model is used to classify an uploaded waste image into one of the supported waste categories.

The model processes the uploaded image and returns:

- Predicted waste category
- Prediction confidence

### 2. YOLO Real-Time Detection

YOLO is used for real-time webcam detection.

The system:

1. Accesses the webcam
2. Captures video frames
3. Processes the frames using the YOLO model
4. Detects waste objects
5. Displays bounding boxes
6. Shows detected category and confidence
7. Allows the user to capture and save the detection

---

## 📂 Project Structure

```text
SmartWaste/
│
├── detection/
│   ├── ai_model.py
│   ├── live_model.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── users/
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── smartwaste/
│   ├── settings.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── model/
│   └── waste_classifier.keras
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
