# Blog API

This project is a simple Blog API built using **Django** and **Django REST Framework**. The Blog API allows users to create, read, update, and delete blog posts and manage comments. This project is designed for learning purposes and can be extended for full-scale production use.

## Features

- User authentication (registration, login, logout)
- CRUD operations for blog posts
- Commenting on posts
- Search functionality for blog posts
- Pagination for large datasets
- JWT token-based authentication for secure access to the API

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Project](#running-the-project)
5. [Testing](#testing)

## Getting Started

Follow the instructions below to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have the following tools installed:

- Python 3.8 or later
- Django 4.0 or later
- Django REST Framework
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SepehrNorouzi7/Blog-API.git
   cd Blog-API
2. Create and activate a virtual environment:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
4. Set up the database:

   ```bash
   python manage.py migrate
5. Create a superuser to access the admin panel:

   ```bash
   python manage.py createsuperuser
6. Run the development server:

   ```bash
   python manage.py runserver

### Running the Project

After following the installation steps, you can run the project on your local machine. Visit http://127.0.0.1:8000/ to interact with the API.
You can access the admin panel via http://127.0.0.1:8000/admin and login using the superuser credentials.

### Testing

To run the tests, use the following command:

   ```bash
   python manage.py test
