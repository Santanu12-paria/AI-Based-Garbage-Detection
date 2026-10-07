# 🗑️ AI-Based Garbage Detection for Smart Waste Management

An AI-powered garbage detection system that uses **YOLO Object Detection** and **Streamlit** to identify and classify different types of waste from images.

The system detects multiple garbage objects in an image and displays their class, confidence score, total count, and overall waste level.

---

## 🎯 Project Objective

The main objective of this project is to develop an intelligent waste detection system that can automatically identify different categories of garbage from images.

This can support smart waste management by helping with:

- Waste identification
- Waste classification
- Garbage monitoring
- Automated waste analysis
- Smart waste management systems

---

## ✨ Features

- 📤 Upload garbage images
- 🤖 YOLO-based object detection
- ♻️ Detect multiple waste categories
- 📊 Class-wise garbage counting
- 🎯 Confidence score for each detection
- 🗑️ Total number of detected objects
- 🚮 Automatic waste-level classification
- 📋 Detection report
- 🖥️ Interactive Streamlit interface

---

## 🧠 Waste Classes

The trained model supports the following waste categories:

1. LDPE
2. Bottle
3. Can
4. Cardboard
5. Organic
6. Paper
7. Plastic

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| YOLO | Object detection |
| Ultralytics | YOLO implementation |
| Streamlit | Web application |
| Pillow | Image processing |
| OpenCV | Computer vision support |
| Git & GitHub | Version control |

---

## 📂 Project Structure

```text
AI-Based-Garbage-Detection/
│
├── app.py
├── check_dataset.py
├── check_9class_distribution.py
├── create_9class_dataset.py
├── README.md
├── .gitignore
│
└── runs/
    └── detect/
        └── garbage_detection-2/
            └── weights/
                └── best.py

---

## ⚙️ System Architecture

```text
Input Image
     ↓
Image Preprocessing
     ↓
YOLO Object Detection
     ↓
Waste Classification
     ↓
Confidence Calculation
     ↓
Object Counting
     ↓
Waste Level Analysis
     ↓
Streamlit Dashboard

🚀 Installation
1. Clone the Repository
Bash

git clone https://github.com/Santanu12-paria/AI-Based-Garbage-Detection.git
2. Open the Project
Bash

cd AI-Based-Garbage-Detection
3. Create a Virtual Environment
Bash

python -m venv venv
4. Activate the Virtual Environment
For Windows PowerShell:

PowerShell

venv\Scripts\Activate.ps1
5. Install Required Libraries
Bash

pip install ultralytics streamlit pillow
▶️ Running the Application
Run the following command:

Bash

streamlit run app.py
The Streamlit application will open in your web browser.

🎯 Detection Configuration
The application currently uses a YOLO confidence threshold of:


0.15
The threshold was selected after testing the model with different garbage images.

📊 Application Features
📷 Original Image
Displays the uploaded garbage image.

🤖 Detection Result
YOLO detects garbage objects and displays bounding boxes around them.

📊 Detection Summary
The application displays:

Total objects detected

Number of waste types

Average confidence

♻️ Waste Classification
The application provides class-wise counts for the detected waste.

📋 Detection Report
Each detected object is displayed with its confidence score.

Example:


Bottle       91.4%
Cardboard    84.7%
Plastic      76.2%
🚮 Waste Level
The application calculates the waste level based on the number of detected objects.

Objects Detected	Waste Level
0–3	🟢 LOW
4–7	🟡 MEDIUM
8+	🔴 HIGH

📈 Results
The system can detect multiple types of garbage from uploaded images.

Supported waste categories include:

LDPE

Bottle

Can

Cardboard

Organic

Paper

Plastic

Detection performance can vary depending on image quality, lighting conditions, object size, and similarity between waste categories.

⚠️ Limitations
Some waste categories have similar visual characteristics.

Small objects may be difficult to detect.

Partially hidden objects may reduce detection performance.

Detection depends on image quality and lighting.

Paper detection can be challenging in some images.

CPU-based inference can be slower than GPU-based inference.

🔮 Future Scope
Future improvements can include:

📱 Mobile application

🌐 Cloud deployment

📹 Real-time camera detection

🚮 Automatic smart-bin classification

📊 Advanced waste analytics

🧠 Larger and more diverse datasets

⚡ GPU acceleration

🔄 Continuous model improvement

🏙️ Integration with smart-city waste management systems

👨‍💻 Project Information
Project Title: AI-Based Garbage Detection for Smart Waste Management

Domain: Deep Learning / Computer Vision

Programming Language: Python

Model: YOLO Object Detection

Framework: Ultralytics YOLO

Web Interface: Streamlit

📜 License
This project is developed for educational and academic purposes.

⭐ Acknowledgement
This project uses the Ultralytics YOLO framework for object detection and Streamlit for developing the interactive web application.

🔗 GitHub Repository
https://github.com/Santanu12-paria/AI-Based-Garbage-Detection



So the order in your README will simply be:

**Project Structure → System Architecture → Installation → Running the Application → Detection Configuration → Application Features → Waste Level → Results → Limitations → Future Scope → Project Information → License → Acknowledgement → GitHub Repository.**





