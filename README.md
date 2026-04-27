# Internship Tracker

A full-stack Flask web application for tracking internship applications, deadlines, statuses, and interview progress.

## Overview

Internship Tracker helps students organize internship applications in one place. Users can save companies, roles, deadlines, notes, and application statuses, then search and filter through their applications.

This project was built to practice full-stack web development using Python, Flask, SQLite, HTML, CSS, and Jinja2 templates.

## Features

- Add, edit, and delete internship applications
- Track application status:
  - Saved
  - Applied
  - Interview
  - Rejected
  - Offer
- Search applications by company or role
- Filter applications by status
- Sort applications by deadline
- Dashboard statistics for application progress
- Interview rate and offer rate analytics
- Deadline status detection:
  - Overdue
  - Due soon
  - On track
- REST API endpoint returning internship data as JSON
- SQLite database for persistent storage
- Responsive user interface

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2

## Project Structure

```text
Internship_Tracker/
├── app.py
├── internships.db
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── edit.html
└── README.md
```

## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/silvanabanica-cmyk/Internship_Tracker.git
cd Internship_Tracker
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

6. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## API Endpoint

The project includes a simple JSON API endpoint:

```text
/api/internships
```

Example response:

```json
[
  {
    "id": 1,
    "company": "Google",
    "role": "Software Engineering Intern",
    "status": "Applied",
    "deadline": "2026-05-10",
    "deadline_status": "Due soon",
    "notes": "Applied through careers page."
  }
]
```

## Future Improvements

- User login and authentication
- Separate application data for each user
- Email or browser deadline reminders
- Calendar view for upcoming deadlines
- CSV export
- Deployment on Render or PythonAnywhere
- More advanced dashboard charts

## What I Learned

- Building a Flask web application
- Using SQLite for database storage
- Creating CRUD functionality
- Handling form submissions
- Filtering, searching, and sorting records
- Rendering dynamic pages with Jinja2
- Creating a simple REST API endpoint
- Designing a responsive dashboard interface