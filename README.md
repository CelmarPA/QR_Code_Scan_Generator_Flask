# 📷 QR Code Generator & Scanner - Flask Web App

A simple and user-friendly Flask web application to generate and scan QR Codes. Built with Python and OpenCV for QR detection and Cloudmersive API for QR generation, it includes image upload, email contact form, and base64 rendering of QR codes.

## 📌 Table of Contents

- [📷 QR Code Generator \& Scanner - Flask Web App](#-qr-code-generator--scanner---flask-web-app)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Features](#-features)
  - [💻 How to Use](#-how-to-use)
  - [▶️ Getting Started](#️-getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Running the Application](#3-running-the-application)
  - [📄 Files](#-files)
  - [🧪 Example](#-example)
  - [✅ License](#-license)
  - [👤 Author](#-author)
  - [💬 Feedback](#-feedback)

---

## 🚀 Features

* QR Code generation from text using Cloudmersive API  
* QR Code scanning from uploaded image using OpenCV  
* Base64 QR code display in browser  
* Image upload and storage in `static/uploads`  
* Responsive contact form with email sending via SMTP  
* Clean and modern interface with sections for Generate, Scan, and Contact

## 💻 How to Use

1. Navigate to the web app.
2. Use the "Generate" section to enter text and generate a QR Code.
3. Use the "Scan" section to upload a QR code image and get its decoded content.
4. Use the "Contact" section to send a message via email.

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/CelmarPA/QR_Code_Scan_Generator_Flask
cd qr_code_scan_generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install Flask opencv-python cloudmersive-barcode-api-client
```

### 3. Running the Application

```bash
python app.py
```

Access via browser at: `http://localhost:5000`

## 📄 Files

* `app.py`: Main Flask application
* `qr_code.py`: QR code generation and scanning logic (Cloudmersive + OpenCV)
* `templates/index.html`: Main HTML interface
* `static/uploads/`: Uploaded QR code images for scanning
* `static/`: Folder containing CSS, images and assets

## 🧪 Example

```plaintext
User enters: "https://example.com"
QR code is displayed as base64 image
User uploads the QR image file
Scanner decodes: "https://example.com"
```

## ✅ License

This project is open-source and free to use for learning or personal projects.

---

## 👤 Author

**Celmar Pereira**

- [GitHub](https://github.com/CelmarPA)
- [LinkedIn](https://linkedin.com/in/celmar-pereira-de-andrade-039830181)
- [Portfolio](https://yourportfolio.com)

---

## 💬 Feedback

Enjoy the app and feel free to suggest improvements or open issues!
