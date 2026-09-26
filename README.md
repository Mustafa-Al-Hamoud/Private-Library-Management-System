# Private Library Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?logo=github)

</p>


---

# Project Overview

This project is a private library management system developed with Python and Streamlit to help manage a personal library in a simple and organized way.

The application was developed as a practical project for a friend named Lian, who needed a digital solution to manage her private library and keep track of books, book copies, friends, and loans.

The system provides an interactive web interface connected to a MySQL database and supports the management of library data through different sections of the application.

---

# Problem / Motivation

Managing a private library with a growing number of books and loans can become difficult when information is tracked manually.

The main challenges include:

- Keeping track of books and individual book copies
- Knowing which copies are currently available or borrowed
- Managing friends who borrow books
- Tracking active and completed loans
- Monitoring due dates and overdue loans
- Maintaining an overview of the library through useful statistics

The goal of this project was to replace manual tracking with a simple digital system that centralizes the library information and makes everyday library management easier.

---

# Project Objectives

The main objectives of the project are:

- Digitize the management of a private library
- Manage books and individual book copies
- Manage friends and their borrowing information
- Create and manage book loans
- Track open and completed loans
- Monitor due dates and overdue loans
- Provide useful statistics through an interactive dashboard
- Store and manage library data using a MySQL database
- Provide a simple and user-friendly web interface

---


# Key Features

The application provides the following main features:

### 📊 Dashboard

- Display key library statistics
- Show monthly loan activity
- Show monthly library spending
- Display all currently open loans
- Highlight overdue and upcoming due dates
- Show the most frequently borrowed books, friends, and authors

### 📚 Book Management

- Add new books and book copies
- Edit book and copy information
- Delete book copies
- Track copy status
- Search and filter books
- Manage multiple copies of the same book

### 👥 Friend Management

- Add new friends
- Edit friend information
- Delete friends when allowed
- Define the maximum number of active loans
- Mark friends as trusted or untrusted
- Search and filter friends

### 🔄 Loan Management

- Create new loans
- Check copy availability before borrowing
- Check the friend's current active loans
- Display open and completed loans
- Finish active loans
- Set the returned copy status to `Available` or `Lost`
- Track loan and due dates
- Handle borrowing confirmations when additional attention is required

---

# Project Workflow

The application follows a layered workflow that connects the user interface, application logic, and database:

```text
User
  │
  ▼
Streamlit Interface
  │
  ▼
Python Application Logic
  │
  ▼
SQLAlchemy
  │
  ▼
MySQL Database
  │
  ▼
Library Data
  ├── Books & Copies
  ├── Friends
  └── Loans
---
```
# Dashboard

The application includes an interactive dashboard that provides an overview of the private library and its activity.

The dashboard includes:

- Total number of books and book copies
- Book copy status distribution
- Monthly loan activity
- Monthly library spending
- Currently open loans
- Due dates and remaining days for open loans
- Top 5 most frequently borrowed books
- Top 5 friends with the most loans
- Top 5 most frequently borrowed authors

Date filters allow the user to analyze loan activity and library spending over a selected period.


---

# Repository Structure

```text
Private-Library-Management-System/
│
├── lianes_lib/
│   │
│   ├── data/
│   │   └── lianes_library_schema_demo_data.sql
│   │
│   ├── images/
│   │
│   ├── src/
│   │   ├── home.py
│   │   ├── connection_string.py
│   │   ├── read_books.py
│   │   ├── insert_books.py
│   │   ├── insert_copies.py
│   │   ├── update_copies.py
│   │   ├── delete_copies.py
│   │   ├── read_friends.py
│   │   ├── insert_friends.py
│   │   ├── update_friends.py
│   │   ├── delete_friends.py
│   │   ├── read_loans.py
│   │   ├── insert_loans.py
│   │   ├── update_loans.py
│   │   └── dashboard_stats.py
│   │
│   └── environment.yml
└── README.md
