import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import time
from GenRE import upload_module, generate_requirements, save_new_requirements

def start_processing():
    """Start the requirement processing in a separate thread."""
    try:
        reset_timer()
        progress_bar.start()
        status_label.config(text="Processing...", fg="blue")

        processing_thread = threading.Thread(target=process_requirements)
        processing_thread.start()
        update_timer(processing_thread)
    except Exception as e:
        progress_bar.stop()
        status_label.config(text="Error: " + str(e), fg="red")

def process_requirements():
    """Main processing function for requirement generation."""
    try:
        global selected_file

        # Validate selected file
        if not selected_file:
            raise FileNotFoundError("No file selected.")

        # Upload and process requirements
        requirements = upload_module(selected_file)
        project_name = project_name_entry.get()
        project_summary = project_summary_entry.get()
        api_key = api_key_entry.get()
        number_requirements = number_requirements_entry.get()

        # Generate new requirements
        new_requirements = generate_requirements(api_key, project_name, project_summary, requirements, number_requirements)

        # Save generated requirements
        output_file = save_new_requirements(new_requirements)

        # Update the status label
        status_label.config(text=f"Processing complete!", fg="green")

        # Update file display
        filename = os.path.basename(output_file)
        results_label.config(text=f"Results saved to: {filename}", fg="blue", cursor="hand2")
        results_label.bind("<Button-1>", lambda e: open_file_location(output_file))
        results_label.bind("<Enter>", lambda e: results_label.config(fg="darkblue"))
        results_label.bind("<Leave>", lambda e: results_label.config(fg="blue"))

        # Display the results
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, new_requirements)

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please select a valid file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        progress_bar.stop()
        stop_timer()

def select_file():
    """Open file dialog to select a file."""
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        selected_file = file_path
        file_label.config(text=f"Selected: {os.path.basename(file_path)}")

def open_file_location(file_path):
    """Open the containing folder with the file selected."""
    folder_path = os.path.dirname(file_path)
    os.startfile(folder_path)

def reset_timer():
    global start_time
    start_time = time.time()
    timer_button.config(text="Time Elapsed: 00:00 seconds", fg="black")

def update_timer(processing_thread):
    if processing_thread.is_alive():
        elapsed_time = time.time() - start_time
        timer_button.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds", fg="black")
        root.after(100, lambda: update_timer(processing_thread))
    else:
        stop_timer()

def stop_timer():
    elapsed_time = time.time() - start_time
    timer_button.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds", fg="green")

def create_gui():
    """Create the GUI interface."""
    global project_name_entry, project_summary_entry, api_key_entry, number_requirements_entry, result_text, file_label, progress_bar, status_label, results_label, timer_button, root

    root = tk.Tk()
    root.title("Self-GenRE - GUI")
    root.minsize(800, 600)

    # Project Name
    tk.Label(root, text="Project Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    project_name_entry = tk.Entry(root, width=70)
    project_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Project Summary
    tk.Label(root, text="Project Summary:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    project_summary_entry = tk.Entry(root, width=70)
    project_summary_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # API Key
    tk.Label(root, text="OpenAI API Key:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    api_key_entry = tk.Entry(root, width=70, show="*")
    api_key_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Number of Requirements
    tk.Label(root, text="Number of Requirements:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    number_requirements_entry = tk.Entry(root, width=70)
    number_requirements_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # File Selection
    tk.Button(root, text="Select File", command=select_file).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    file_label = tk.Label(root, text="No file selected", fg="gray")
    file_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Timer Button
    timer_button = tk.Button(root, text="Time Elapsed: 00:00 seconds", state="disabled", relief="raised", fg="black")
    timer_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    # Start Processing Button
    tk.Button(root, text="Start Processing", command=start_processing).grid(row=6, column=0, columnspan=2, pady=10, sticky="n")

    # Progress Bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=600)
    progress_bar.grid(row=7, column=0, columnspan=2, pady=5)

    # Status Label
    status_label = tk.Label(root, text="", fg="blue")
    status_label.grid(row=8, column=0, columnspan=2, pady=5)

    # Results Display
    tk.Label(root, text="Results:").grid(row=9, column=0, padx=10, pady=5, sticky="nw")
    result_text = tk.Text(root, height=20, width=80, wrap="word")
    result_text.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    # Results Filename
    results_label = tk.Label(root, text="", fg="blue")
    results_label.grid(row=10, column=0, columnspan=2, pady=5, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    selected_file = None
    start_time = 0
    create_gui()
