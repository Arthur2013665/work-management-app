# Worker Management App
This is a worker management application that allows you to manage worker data, including creating worker files, adding workers, marking attendance, and viewing or deleting worker information. The app requires a valid license key for full functionality.

# Features
Create Worker Files: Create a new worker file with the required columns (Name, Salary, Attendance).
Add Workers: Add new workers to a selected file with their name and salary.
Mark Attendance: Mark attendance for workers (increments attendance by 1 each time).
View Workers: View the list of workers in the selected file.
Delete Worker Files: Delete existing worker files from the app.
License Activation: The app requires a valid license key to unlock full features. If no license is provided or invalid, the app operates in demo mode.
# Installation
Clone or Download the Repository: Download or clone the project to your local machine.

git clone <https://github.com/Arthur2013665/work-management-app/edit/main/README.md>

bash
Copy
Edit
git clone <repository-url>
Install Dependencies: This project uses Python's built-in libraries, so there are no external dependencies required. Ensure you have Python 3.x installed on your machine.

# Run the Application: Navigate to the project directory and run the main Python script:

if u want to run it paste this command in your terminal or follow instructions: python app.py

bash
Copy
Edit
python main.py
The app will display a loading screen, after which it will either prompt you to enter a valid license key or proceed in demo mode.

# License Management
The app requires a license key to unlock full functionality.
To activate the app, enter a valid license key when prompted.
The app will store the license key in a file (user_license.txt) for future use.
Usage
Creating a Worker File:

# Enter the desired worker file name.
Click on "Create Worker File". The file will be created with the required columns.
Adding Workers:

# Enter the worker's name and salary.
Click "Add Worker" to add the worker to the selected file.
Marking Attendance:

# Enter the worker's name and select the file.
Click "Mark Attendance" to increment the worker's attendance.
Viewing Workers:

# Select a worker file and click "View Workers".
The list of workers will be displayed in a read-only text box.
Deleting Worker File:

# Select a worker file and click "Delete Worker File".
The selected worker file will be permanently deleted.
Demo Mode vs Activated Mode
Demo Mode: If a valid license is not entered, the app operates in demo mode. In this mode, only limited features may be available.
Activated Mode: After entering a valid license key, all features of the app are unlocked.

# This project is licensed under the MIT License - see the LICENSE file for details.

