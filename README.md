# Dojo Training Manual PWA

An interactive Progressive Web App (PWA) for martial arts dojos, digitizing the physical training manual. This app provides students with a modern, installable, and interactive experience for learning techniques, reviewing curriculum, and accessing official resources.

![Sign In](https://media.licdn.com/dms/image/v2/D562DAQG3YbCTcWs0sQ/profile-treasury-image-shrink_800_800/B56ZfHF9YCGQAY-/0/1751391937854?e=1752872400&v=beta&t=o_TlJj9K2CyCvAL5WasAf63jxRoph6AtFeEQfnppG7Q)

![Belt Selection](https://media.licdn.com/dms/image/v2/D562DAQFxh6r1g9GA-w/profile-treasury-image-shrink_800_800/B56ZfHGHHdH8Ac-/0/1751391982382?e=1752872400&v=beta&t=TtEyJQvEGyCZYE2fabt1PvQ6xFPgPz4YRpIZSI5xWoQ)

![Embedded PDF Viewer](https://media.licdn.com/dms/image/v2/D562DAQEUk6B4hARxPA/profile-treasury-image-shrink_800_800/B56ZfHGPTpGoAc-/0/1751392034079?e=1752872400&v=beta&t=h8qJJiIdNyKgYfZ8lnIkg19Mq3k6NUBMBpcabTBd7rs)

![Technique Browser](https://media.licdn.com/dms/image/v2/D562DAQE8QnOp6_MLcg/profile-treasury-image-shrink_800_800/B56ZfHGdCKGQAc-/0/1751392080342?e=1752872400&v=beta&t=HqObEMdq74L1Go8oM7qSuTs5LIMWyuZOPVFQJTXMIjQ)

![Flashcard View](https://media.licdn.com/dms/image/v2/D562DAQGZ1eZT85OoaA/profile-treasury-image-shrink_800_800/B56ZfHGw8LGoBo-/0/1751392140743?e=1752872400&v=beta&t=aUEXFVBNeXd4UioIjSW11a8D2ywj0NyCQvEm4SkvfgM)


---

## Features

- **Progressive Web App:** Installable on desktop and mobile, with offline support.
- **Dynamic "Belt Rack" Dashboard:** A visually engaging main menu for belt selection.
- **Dynamic Color Theming:** The UI automatically adapts to the selected belt's color scheme.
- **Belt-by-Belt Curriculum:** Organized by belt rank, from beginner to advanced.
- **Interactive Flashcards:** Practice techniques in browse and randomized quiz modes.
- **Embedded PDF Manuals:** View official belt manuals directly in the app.
- **Video Demonstrations:** Native video for each technique (no external links).
- **Secure Authentication:** Google Sign-in with admin approval for new users.
- **Admin Interface:** Manage users, techniques, and content via Django admin.

---

## Technology Stack

- **Backend:** Python 3.12, Django 5.2
- **Database:** PostgreSQL (Cloud SQL in production, SQLite for local dev)
- **Frontend:** HTML, Tailwind CSS (via CDN), Vanilla JavaScript (PWA features)
- **Authentication:** Google Identity Platform (`django-allauth`)
- **Media Storage:** Google Cloud Storage (PDFs, videos)
- **Hosting:** Google Cloud Run (serverless containers)
- **Containerization:** Docker, Gunicorn (WSGI server)

---

## Local Development Setup

1. **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd dojo-pwa
    ```

2. **Create and Activate a Virtual Environment**
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    - Create a `.env` file in the project root:
      ```
      DEBUG=True
      SECRET_KEY='your-local-secret-key'
      DATABASE_URL='sqlite:///db.sqlite3'
      ```
    - For Google authentication, add your credentials as needed.

5. **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Data Import

Bulk-import techniques using a custom Django management command.

- **Format:** Each line in the `.txt` file:  
  `"Technique Name";"Technique Description"`
- **Usage:**
    ```bash
    python manage.py import_techniques "Belt Name" "/path/to/cards.txt"
    ```

---

## Production Deployment

- **Containerization:**  
  The app is containerized with Docker. See the `Dockerfile` for build steps.
- **Static Files:**  
  Static files are collected at build time (`collectstatic`).
- **WSGI Server:**  
  Gunicorn serves the app in production.
- **Cloud Run:**  
  Deploy the container to Google Cloud Run. The app auto-detects Cloud Run and uses production settings.

---

## Environment Variables

- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`:  
  Used for automated superuser creation in production.
- `DATABASE_URL`:  
  Connection string for your database.
- `SECRET_KEY`:  
  Django secret key.
- `DEBUG`:  
  Set to `False` in production.
- Google authentication and storage credentials as required.

---

## Project Structure

- `belts/` – Models, views, and commands for belt techniques and curriculum.
- `core/` – Core app, admin, and management commands.
- `users/` – User management and authentication.
- `templates/` – HTML templates for the PWA and admin.
- `static/` – Static assets (icons, CSS, JS).
- `Charts/` – Official PDF manuals for each belt.
- `manage.py` – Django management utility.
- `Dockerfile` – Container build instructions.
- `requirements.txt` – Python dependencies.

---

## License

This project is licensed under the Apache 2.0 License.

