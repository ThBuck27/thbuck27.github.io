# Grazioso Salvare Dashboard  
## CS 499 Database Enhancement

## Project Overview

This project is an enhanced version of the Grazioso Salvare animal-shelter dashboard originally created for CS 340. The application uses Python, MongoDB, PyMongo, Pandas, and Dash to retrieve, filter, and display animal records.

The dashboard allows users to select one of the following rescue categories:

- Water Rescue
- Mountain or Wilderness Rescue
- Disaster or Individual Tracking
- Reset

The selected filter updates an interactive data table, pie chart, and map.

A reusable `AnimalShelter` CRUD module handles communication between the dashboard and MongoDB.

---

## Enhancement Summary

The CS 499 database enhancement improves the original artifact by adding:

- A configurable MongoDB connection
- Removal of hard-coded course credentials from the enhanced notebook
- Immediate connection verification using a MongoDB `ping`
- Query validation for approved fields, operators, and value types
- Protection against empty update and delete queries
- A compound index for common rescue-filter fields
- Automated database connection and query-validation tests
- A repeatable local mock-database setup
- Compatibility updates for the current Dash and Jupyter environment

The goal of the enhancement was to improve the artifact's portability, security, reliability, and testability while preserving the original dashboard behavior.

---

## Technologies Used

- Python
- MongoDB
- PyMongo
- Pandas
- NumPy
- Dash
- Plotly
- Dash DataTable
- Dash Leaflet
- Jupyter Notebook

---

## Project Files

```text
Enhanced/
-CRUD_Python_Module.py
-ProjectTwoDashboard.ipynb
-seed_local_database.py
-test_database_connection.py
-test_query_validation.py
-Enhancement_Three_Testing_Notes.txt
-Grazioso Salvare Logo.png
-README.md