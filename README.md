Mini Cloud Storage – Flask Web App

Mini Cloud Storage is a lightweight cloud-style file storage web application built using Flask (Python).
In this project, the user’s own laptop or PC acts as the server, hosting the application and storing uploaded files locally.
It allows users to upload, view, and download files through a modern glassmorphism-based UI.
The entire application is implemented in a single Python file with no database and no authentication.

Features

File upload using drag-and-drop or file picker

Display uploaded files with filename and size (KB / MB)

Secure file download functionality

Laptop or PC functions as the local server

Files are stored on the same machine running the application

Modern glassmorphism user interface

Dark gradient background with cloud-style animations

Animated gradient headings and smooth hover effects

Custom cursor effects

Fully responsive and mobile-friendly design

No database required

No authentication required

Single-file Flask application

Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS, JavaScript (embedded directly in Flask)

Server: Local machine (Laptop or PC)

Storage: Local filesystem (storage/ directory)

Project Structure
mini-cloud-storage/

│

├── app.py          Main Flask application

├── storage/        Uploaded files (auto-created)

└── README.md       Project documentation

How It Works

The Flask application runs on the user's local laptop or PC

This local machine acts as the server

Uploaded files are saved directly to the server’s local storage

Other devices on the same network can access the app using the server’s IP address

Getting Started
Prerequisites

Python 3.8 or higher

A laptop or PC to act as the server

Check Python installation:

python --version

Installation

Install Flask:

pip install flask

Running the Application

Start the Flask server:

python app.py


The application will be accessible at:

http://localhost:8000


For access from other devices on the same network:

http://<server-ip>:8000

Application Routes
Route	Method	Description
/	GET	Home page with file upload and file list
/upload	POST	Handles file uploads
/files/<filename>	GET	Downloads a selected file
Storage Behavior

Files are stored in the storage/ directory on the server machine

The directory is created automatically on application startup

File sizes are displayed dynamically in KB or MB

User Interface Highlights

Glassmorphism cards with blur and transparency

Animated gradient headings

Drag-and-drop upload zone

Smooth hover animations and transitions

Responsive layout for desktop and mobile devices

Limitations

This project is designed for learning and small-scale use:

No user authentication

No file deletion or file management

No file type or size validation

Local machine storage only

Possible Enhancements

User authentication system

File delete and rename options

File size and type restrictions

Upload progress indicator

Deployment on a cloud server or VPS

Multi-user support

License

This project is open source and free to use for educational and personal projects.

Author

Developed as a Flask-based learning and demonstration project.
Feel free to fork the repository and build upon it.
