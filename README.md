# Dojo Training Manual PWA

This project is an interactive Progressive Web App (PWA) designed to digitize a martial arts dojo's physical training manual. It serves as both a practical training tool for students and a comprehensive demonstration of full-stack web development and cloud deployment using a modern Python and Google Cloud Platform stack.

## Key Features

* **Progressive Web App (PWA):** Installable on any device (desktop or mobile) for an app-like experience and offline capabilities.
* **Belt-by-Belt Curriculum:** Content is organized logically by belt rank, from beginner to advanced levels.
* **Interactive Flashcards:** Practice techniques in two modes:
    * **Browse Mode:** Sequentially review all techniques for a given belt.
    * **Randomized Mode:** Test your knowledge with flashcards that present techniques in a random order.
* **Embedded PDF Manuals:** Access the complete, official PDF manual for any belt level directly within the app.
* **Video Demonstrations:** Each technique is accompanied by a native video demonstration (no external YouTube links).
* **Secure Authentication:** User signup is handled via Google Sign-in, with a manual admin approval system for new students.

## Technology Stack

* **Backend:** Python 3.12, Django 5.2
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, Vanilla JavaScript (for PWA and interactivity)
* **Cloud Platform:** Google Cloud Platform (GCP)
* **Hosting:** Google Cloud Run (Serverless Containers)
* **DB Hosting:** Google Cloud SQL for PostgreSQL
* **Media Storage:** Google Cloud Storage (for PDFs & Videos)
* **Authentication:** Google Identity Platform (via `django-allauth`)
* **WSGI Server:** Gunicorn
* **Containerization:** Docker

## Local Development Setup

To run this project on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd dojo-pwa
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    * Create a `.env` file in the project root.
    * Add the following basic configuration:
        ```
        DEBUG=True
        SECRET_KEY='a-local-secret-key'
        DATABASE_URL='sqlite:///db.sqlite3'
        ```

5.  **Run Database Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The app will be available at `http://127.0.0.1:8000/`.

## Data Import

The project includes a custom Django management command to bulk-import techniques from a properly formatted text file.

* **Format:** A `.txt` file with each line containing `"Technique Name";"Technique Description"`.
* **Usage:**
    ```bash
    python manage.py import_techniques "Belt Name" "/path/to/your/cards.txt"
    ```