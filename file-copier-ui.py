import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path
import threading
import re

class FileCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Extension Copier")
        self.root.geometry("800x600")
        
        # Variables
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.new_extension = tk.StringVar()
        self.extensions = set()
        self.is_copying = False
        
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Path selection
        ttk.Label(main_frame, text="Source Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.source_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2)
        
        ttk.Label(main_frame, text="Destination Folder:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.dest_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2)
        
        # Extension management
        ext_frame = ttk.LabelFrame(main_frame, text="Extensions", padding="5")
        ext_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(ext_frame, text="Add Extension:").grid(row=0, column=0, sticky=tk.W)
        self.ext_entry = ttk.Entry(ext_frame, textvariable=self.new_extension, width=20)
        self.ext_entry.grid(row=0, column=1, padx=5)
        ttk.Button(ext_frame, text="Add", command=self.add_extension).grid(row=0, column=2)
        
        # Extensions list
        self.ext_listbox = tk.Listbox(ext_frame, width=30, height=5)
        self.ext_listbox.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(ext_frame, text="Remove Selected", command=self.remove_extension).grid(row=1, column=2)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Status
        self.status_text = tk.Text(main_frame, height=10, width=60, wrap=tk.WORD)
        self.status_text.grid(row=4, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))
        
        # Scrollbar for status
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Copying", command=self.start_copying)
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel_copying).grid(row=0, column=1, padx=5)
        
        # Add .nk and .autosave as default extensions
        self.extensions.add('.nk')
        self.extensions.add('.autosave')
        self.update_extension_list()
        
    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_path.set(folder)
            
    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_path.set(folder)
            
    def add_extension(self):
        ext = self.new_extension.get().strip()
        if not ext:
            return
            
        # Add leading dot if not present
        if not ext.startswith('.'):
            ext = '.' + ext
            
        # Validate extension format
        if not re.match(r'^\.[a-zA-Z0-9]+$', ext):
            messagebox.showerror("Error", "Invalid extension format")
            return
            
        self.extensions.add(ext.lower())
        self.new_extension.set('')
        self.update_extension_list()
        
    def remove_extension(self):
        selection = self.ext_listbox.curselection()
        if selection:
            ext = self.ext_listbox.get(selection[0])
            self.extensions.remove(ext)
            self.update_extension_list()
            
    def update_extension_list(self):
        self.ext_listbox.delete(0, tk.END)
        for ext in sorted(self.extensions):
            self.ext_listbox.insert(tk.END, ext)
            
    def update_status(self, message):
        self.status_text.insert(tk.END, message + '\n')
        self.status_text.see(tk.END)
        
    def copy_files(self):
        source_dir = Path(self.source_path.get())
        dest_dir = Path(self.dest_path.get())
        
        # Add initial status update
        self.update_status(f"Starting copy operation...")
        self.update_status(f"Source: {source_dir}")
        self.update_status(f"Destination: {dest_dir}")
        self.update_status(f"Extensions: {', '.join(self.extensions)}")
        
        try:
            # Count total files for progress bar
            self.update_status("Counting files to copy...")
            files_to_copy = list(self.find_files(source_dir))  # Convert to list to get actual files
            total_files = len(files_to_copy)
            
            if total_files == 0:
                self.update_status("No matching files found!")
                return
                
            self.update_status(f"Found {total_files} files to copy")
            copied_files = 0
            
            for source_file in self.find_files(source_dir):
                if not self.is_copying:
                    break
                    
                # Get relative path and create destination path
                rel_path = source_file.relative_to(source_dir)
                dest_file = dest_dir / rel_path
                
                # Create destination directory if needed
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(source_file, dest_file)
                copied_files += 1
                
                # Update progress
                progress = (copied_files / total_files) * 100
                self.progress_var.set(progress)
                
                # Update status
                self.root.after(0, self.update_status, f"Copied: {rel_path}")
            
            if self.is_copying:
                self.root.after(0, self.update_status, "\nCopy completed successfully!")
            else:
                self.root.after(0, self.update_status, "\nCopy operation cancelled.")
                
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
            
        finally:
            self.is_copying = False
            self.root.after(0, self.start_button.configure, {"state": "normal"})
            
    def find_files(self, source_dir):
        if not os.path.exists(source_dir):
            self.update_status(f"Error: Source directory {source_dir} does not exist!")
            return
            
        found_files = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                if any(file.lower().endswith(ext.lower()) for ext in self.extensions):
                    found_files.append(Path(root) / file)
        return found_files
                    
    def start_copying(self):
        if not self.source_path.get() or not self.dest_path.get():
            messagebox.showerror("Error", "Please select both source and destination folders")
            return
            
        if not self.extensions:
            messagebox.showerror("Error", "Please add at least one file extension")
            return
            
        self.is_copying = True
        self.start_button.configure(state="disabled")
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        
        # Start copying in a separate thread
        threading.Thread(target=self.copy_files, daemon=True).start()
        
    def cancel_copying(self):
        self.is_copying = False

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopierApp(root)
    root.mainloop()
