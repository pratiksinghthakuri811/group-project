# group-project
Match Management System
Project Description
The Match Management System is a desktop application developed using Python, Tkinter, and SQLite.
It is designed to manage football match records in a structured and user-friendly way.
The system allows users to schedule matches, update scores, calculate results automatically, and store match data permanently in a database.

Objectives
To develop a GUI-based desktop application
To implement CRUD operations (Create, Read, Update, Delete)
To integrate a relational database using SQLite
To apply basic logic for sports statistics calculation

Technologies Used
Python 3
Tkinter (Graphical User Interface)
SQLite3 (Database Management)
Datetime module

System Features
Schedule new matches
View all scheduled matches in a table
Update match scores
Automatically calculate match result (Win, Loss, Draw)
Calculate and display season win rate
Delete match records
Store and retrieve data from SQLite database

Database Structure
Table Name: matches
Fields:
id (Integer, Primary Key, Auto Increment)
opponent (Text)
match_date (Text)
venue (Text)
team_score (Integer, Default 0)
opponent_score (Integer, Default 0)

System Workflow
User enters opponent name, match date, and venue.
The system stores match details in the database.
Scores can be updated after the match.
The system automatically determines the result.
Win rate is calculated based on stored match records.
