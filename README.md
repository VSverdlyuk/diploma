# Diploma Project

This project consists of three different web applications built using Flask, Django, and FastAPI. Each application serves the purpose of managing books, with features like viewing, creating, editing, and deleting books.

## Getting Started

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/VSverdlyuk/diploma.git
cd diploma
```

### 2. Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
Copy code
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies
Install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

Once the dependencies are installed, you can run each application independently by following the instructions below.

## 1. Flask Application
To start the Flask application, navigate to the book_manager_flask directory:

```bash
cd book_manager_flask
python app.py
```

The Flask application will start running locally, typically accessible at http://127.0.0.1:5000/.

## 2. Django Application
To start the Django application, navigate to the library_project directory:

```bash
cd library_project
python manage.py runserver
```

The Django application will start running locally, typically accessible at http://127.0.0.1:8000/.

## 3. FastAPI Application
To start the FastAPI application, navigate to the library_app_fastapi directory:

```bash
cd library_app_fastapi
uvicorn main:app --reload
```

The FastAPI application will start running locally, typically accessible at http://127.0.0.1:8000/.

