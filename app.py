import os
import random
import string
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter.ttk import Progressbar

# Set the default app folder (no need to ask the user)
APP_FOLDER = "./work_management"
MAHK_EXTENSION = ".mahk"
LICENSE_FILE = os.path.join(APP_FOLDER, "licenses.lince")
USER_LICENSE_FILE = "user_license.txt"  # File to store the user-entered license

# Ensure app directory exists
os.makedirs(APP_FOLDER, exist_ok=True)

def generate_license_keys(count=10000):
    """Generates unique license keys."""
    keys = []
    for _ in range(count):
        key = "-".join(
            ["".join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(4)]
        )
        keys.append(key)
    return keys

def save_licenses():
    """Creates a license file if it doesn't exist."""
    if not os.path.exists(LICENSE_FILE):
        keys = generate_license_keys()
        with open(LICENSE_FILE, "w") as f:
            f.write("\n".join(keys))

def validate_license(user_key):
    """Validates user input against stored license keys."""
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            keys = f.read().splitlines()
            return user_key in keys
    return False

def load_user_license():
    """Loads the saved license from user_license.txt."""
    if os.path.exists(USER_LICENSE_FILE):
        with open(USER_LICENSE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_user_license(license_key):
    """Saves the valid license to user_license.txt."""
    with open(USER_LICENSE_FILE, "w") as f:
        f.write(license_key)

def prompt_license():
    """Prompts the user for a license key if none is provided."""
    user_license = load_user_license()
    if user_license:
        # If a valid license is already saved, return it
        if validate_license(user_license):
            license_key.set(user_license)
            messagebox.showinfo("Valid License", "The license key is valid!")
            update_title(True)  # Set title to without "(Demo)"
            return True
        else:
            update_title(False)  # Set title to with "(Demo)"
            return False
    else:
        if messagebox.askyesno("License Required", "License key is required. Would you like to enter one now?"):
            key = simpledialog.askstring("License Key", "Enter your license key:")
            if validate_license(key):
                save_user_license(key)  # Save the entered license key
                license_key.set(key)
                messagebox.showinfo("Valid License", "The license key is valid!")
                update_title(True)  # Set title to without "(Demo)"
                return True
            else:
                messagebox.showerror("Invalid License", "The entered license key is invalid.")
                update_title(False)  # Set title to with "(Demo)"
                return False
        update_title(False)  # Set title to with "(Demo)"
        return False

def update_title(is_activated):
    """Update the window title based on license status."""
    if is_activated:
        root.title("Worker Management App")
    else:
        root.title("Worker Management App (Demo)")

def create_worker_file():
    """Creates a new worker file."""
    if not prompt_license():
        return
    filename = file_entry.get()
    if filename:
        file_path = os.path.join(APP_FOLDER, filename + MAHK_EXTENSION)
        with open(file_path, "w") as f:
            f.write("Name,Salary,Attendance\n")
        messagebox.showinfo("Success", f"Worker file '{filename}{MAHK_EXTENSION}' created.")

def add_worker():
    """Adds a worker to the specified file."""
    if not prompt_license():
        return
    filename = file_entry.get()
    name = name_entry.get()
    salary = salary_entry.get()
    file_path = os.path.join(APP_FOLDER, filename + MAHK_EXTENSION)
    if os.path.exists(file_path) and name and salary:
        with open(file_path, "a") as f:
            f.write(f"{name},{salary},0\n")
        messagebox.showinfo("Success", "Worker added successfully.")
    else:
        messagebox.showerror("Error", "File does not exist or invalid data.")

def mark_attendance():
    """Marks attendance for a given worker."""
    if not prompt_license():
        return
    filename = file_entry.get()
    worker_name = name_entry.get()
    file_path = os.path.join(APP_FOLDER, filename + MAHK_EXTENSION)
    if os.path.exists(file_path) and worker_name:
        lines = []
        with open(file_path, "r") as f:
            lines = f.readlines()
        with open(file_path, "w") as f:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == worker_name and len(data) == 3:
                    data[2] = str(int(data[2]) + 1)
                f.write(",".join(data) + "\n")
        messagebox.showinfo("Success", f"Attendance marked for {worker_name}.")
    else:
        messagebox.showerror("Error", "File does not exist or invalid worker name.")

def view_workers():
    """Displays workers in the selected file."""
    if not prompt_license():
        return
    filename = file_entry.get()
    file_path = os.path.join(APP_FOLDER, filename + MAHK_EXTENSION)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            workers = f.read()
        worker_text.config(state=tk.NORMAL)  # Enable editing to insert data
        worker_text.delete("1.0", tk.END)
        worker_text.insert(tk.END, workers)
        worker_text.config(state=tk.DISABLED)  # Make it read-only again
    else:
        messagebox.showerror("Error", "File does not exist.")

def delete_worker_file():
    """Deletes a worker file."""
    if not prompt_license():
        return
    filename = file_entry.get()
    file_path = os.path.join(APP_FOLDER, filename + MAHK_EXTENSION)
    if os.path.exists(file_path):
        os.remove(file_path)
        messagebox.showinfo("Success", f"Worker file '{filename}{MAHK_EXTENSION}' deleted.")
    else:
        messagebox.showerror("Error", "File does not exist.")

def loading_screen():
    """Displays a loading screen with a progress bar."""
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")
    loading_window.geometry("400x150")
    
    label = tk.Label(loading_window, text="Loading... Please wait", font=("Arial", 14))
    label.pack(pady=10)
    
    # Create a Progressbar widget
    progress = Progressbar(loading_window, orient="horizontal", length=300, mode="determinate", maximum=100)
    progress.pack(pady=20)
    
    # Function to update the progress bar
    def update_progress(i=0):
        progress["value"] = i
        if i < 100:
            root.after(50, update_progress, i + 2)  # Increment every 50ms
        else:
            # After 5 seconds (100% progress), initialize the app
            root.after(500, lambda: initialize_app(loading_window))
    
    # Start the progress update
    update_progress()

def initialize_app(loading_window):
    """Initialize the main app after the loading screen."""
    save_licenses()  # Ensure the license file exists
    loading_window.destroy()  # Close the loading screen
    
    # Create the main window for the app
    global license_key, file_entry, worker_text, name_entry, salary_entry
    
    license_key = tk.StringVar()

    # Add a "Enter License" Button
    license_button = tk.Button(root, text="Enter License", command=enter_license)
    license_button.pack(pady=10)

    tk.Label(root, text="Enter Worker File Name:").pack()
    file_entry = tk.Entry(root)
    file_entry.pack()

    tk.Label(root, text="Worker Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Salary:").pack()
    salary_entry = tk.Entry(root)
    salary_entry.pack()

    add_worker_button = tk.Button(root, text="Add Worker", command=add_worker)
    add_worker_button.pack()

    delete_worker_button = tk.Button(root, text="Delete Worker File", command=delete_worker_file)
    delete_worker_button.pack()

    # Disable other features initially
    add_worker_button.config(state=tk.NORMAL)  # Enable Add Worker Button
    delete_worker_button.config(state=tk.NORMAL)  # Enable Delete Worker Button

    mark_attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance, state=tk.DISABLED)
    mark_attendance_button.pack()
    view_workers_button = tk.Button(root, text="View Workers", command=view_workers, state=tk.DISABLED)
    view_workers_button.pack()

    worker_text = tk.Text(root, height=10, width=50)
    worker_text.pack()

    # Disable editing (make it read-only)
    worker_text.config(state=tk.DISABLED)

    root.deiconify()  # Show the main window

def enter_license():
    """Prompts the user to enter the license key."""
    license_key_input = simpledialog.askstring("License Key", "Enter your license key:")
    if validate_license(license_key_input):
        save_user_license(license_key_input)  # Save the entered license key
        license_key.set(license_key_input)
        messagebox.showinfo("Valid License", "The license key is valid!")
        enable_features()
    else:
        messagebox.showerror("Invalid License", "The entered license key is invalid.")

def enable_features():
    """Enables features that require a valid license."""
    # Enable features that require a valid license
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(state=tk.NORMAL)  # Enable all buttons

    worker_text.config(state=tk.NORMAL)  # Allow the worker_text widget to be updated

# Create the root window first (but don't show it yet)
root = tk.Tk()
root.withdraw()  # Hide the main window

# Display the loading screen
loading_screen()

# Start the main loop for the loading screen
root.mainloop()
