![Banner Image](/markdown-image-files/WEB_SERVICES_AND_APPLICATIONS.png)
---
![GitHub last commit](https://img.shields.io/github/last-commit/damienfarrell/wsaa-project)
![GitHub contributors](https://img.shields.io/github/contributors/damienfarrell/wsaa-project)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/damienfarrell/wsaa-project)

This repository contains the project for the Web Services and Applications module as part of the HDip in Data Analytics at ATU.

# **WSAA Project**
---

### **Project Brief**

> Write a program that demonstrates that you understand creating and consuming RESTful APIs. I will allow a lot of flexibility in this project, so that you can use it as an opportunity to do something that is useful for your work.
> 
> If you cannot think of a project to do:
> - Create a Web application in Flask that has a RESTful API.
> - The application should link to one or more database tables.
> - You should also create web pages that can consume the API, i.e., perform CRUD operations on the data.

### **Project Details**

This project is a web application built using FastAPI( I hope that was ok), SQLAlchemy, PostgreSQL, Jinja2 & HTMX . It is a RESTful API and web pages to perform CRUD operations on a film watch list.

The front end has a ton of bugs and issues. Just refresh often. The back end is pretty solid unless I broke it in the last few hours.

### Hosting

It does not work. Could not use PythonAnywhere as FastAPI is not supported which came around to bite me in the butt. Set up a VM on Digital Ocean but I have ran out of time and the app does not work.

**Live Application**: [http://143.110.162.143:8000/](http://143.110.162.143:8000/)

**API Documentation**:
- Swagger UI: [http://143.110.162.143:8000/docs#/](http://143.110.162.143:8000/docs#/)
- ReDoc: [http://143.110.162.143:8000/redoc](http://143.110.162.143:8000/redoc)

## Features

- User registration and login
- Add films to watch list
- Mark films as watched and rate them
- Persistent user sessions with JWT tokens

## Packages Used

### Backend

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL**: Relational database to store user and film data.

### Frontend

- **HTML & CSS**: Structure and styling of the web pages.
- **PicoCSS**: Minimal CSS framework for styling.
- **HTMX**: A library that allows accessing AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly in HTML.
- **SweetAlert2**: A beautiful, responsive, customizable replacement for JavaScript's popup boxes.

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/film-watch-list.git
    cd film-watch-list
    ```
2. **Build and run the application**:

    ```sh
    docker-compose up --build
    ```

    This will build the Docker images and start the containers for the FastAPI app, Alembic (for database migrations), and PostgreSQL.

3. **Access the application**:

    Open your browser and navigate to `http://localhost:8000` to access the application.

## Project Structure

- `app/`: Contains the FastAPI application code.
    - `api/`: Contains the API routes.
    - `database.py`: Database setup and session management.
    - `models.py`: SQLAlchemy models for database tables.
    - `schemas.py`: Pydantic models for data validation.
    - `utils.py`: Utility functions such as password hashing.
    - `main.py`: Entry point for the FastAPI application.
- `templates/`: Contains Jinja2 templates for rendering HTML pages.
- `partials/`: Contains partial HTML templates for HTMX responses.
- `Dockerfile`: Docker configuration for the FastAPI app.
- `docker-compose.yml`: Docker Compose configuration for the multi-container setup.

## API Endpoints

### Authentication

- `POST /login`: Login with email and password.
- `POST /users`: Register a new user.

### Films

- `GET /films/`: Get a list of films.
- `POST /films/`: Add a new film.
- `GET /films/{id}`: Get details of a specific film.
- `DELETE /films/{id}`: Delete a film.
- `PUT /films/{id}`: Update film details.

### **References**

- [Python API Development - Comprehensive Course for Beginners](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- [How to Use FastAPI: A Detailed Python Tutorial](https://www.youtube.com/watch?v=SORiTsvnU28)
- [SQLAlchemy: The BEST SQL Database Library in Python](https://www.youtube.com/watch?v=aAy-B6KPld8)
- [FastAPI with Jinja2 in UNDER 6 minutes](https://www.youtube.com/watch?v=92iCfXAK0Gc)
- [FastAPI Python framework - Returning HTML templates (with HTMX integration)](https://www.youtube.com/watch?v=yu0TbJ2BQso)
- [FastAPI Python framework - SQLAlchemy and Database integration](https://www.youtube.com/watch?v=8SPF6TBVj28)
- [How I deploy serverless containers for free](https://www.youtube.com/watch?v=cw34KMPSt4k)