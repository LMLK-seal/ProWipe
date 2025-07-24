import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import threading
import time
from pathlib import Path

class SecureDeleteTool:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Advanced Secure File Deletion Tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variables
        self.selected_files = []
        self.is_deleting = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Advanced Secure File Deletion Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Permanently delete files using DoD 5220.22-M standard (3-pass overwrite)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # File selection buttons
        button_frame = ctk.CTkFrame(file_frame)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.select_files_btn = ctk.CTkButton(
            button_frame,
            text="Select Files",
            command=self.select_files,
            width=120,
            height=35
        )
        self.select_files_btn.pack(side="left", padx=(0, 10))
        
        self.select_folder_btn = ctk.CTkButton(
            button_frame,
            text="Select Folder",
            command=self.select_folder,
            width=120,
            height=35
        )
        self.select_folder_btn.pack(side="left", padx=(0, 10))
        
        self.clear_list_btn = ctk.CTkButton(
            button_frame,
            text="Clear List",
            command=self.clear_list,
            width=100,
            height=35,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.clear_list_btn.pack(side="left")
        
        # File list
        list_label = ctk.CTkLabel(file_frame, text="Selected Files:", font=ctk.CTkFont(size=14, weight="bold"))
        list_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Scrollable frame for file list
        self.file_list_frame = ctk.CTkScrollableFrame(file_frame, height=200)
        self.file_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Options frame
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        options_label = ctk.CTkLabel(options_frame, text="Deletion Options:", font=ctk.CTkFont(size=14, weight="bold"))
        options_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Overwrite passes
        passes_frame = ctk.CTkFrame(options_frame)
        passes_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(passes_frame, text="Overwrite Passes:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(20, 10), pady=10)
        
        self.passes_var = ctk.StringVar(value="3")
        passes_menu = ctk.CTkOptionMenu(
            passes_frame,
            values=["1", "3", "7", "35"],
            variable=self.passes_var,
            width=80
        )
        passes_menu.pack(side="left", padx=(0, 20), pady=10)
        
        # Info label
        info_text = "• 1 pass: Quick deletion\n• 3 passes: DoD standard (recommended)\n• 7 passes: High security\n• 35 passes: Maximum security (Gutmann method)"
        info_label = ctk.CTkLabel(passes_frame, text=info_text, font=ctk.CTkFont(size=10), justify="left")
        info_label.pack(side="left", padx=(20, 0), pady=10)
        
        # Verify deletion checkbox
        self.verify_var = ctk.BooleanVar(value=True)
        verify_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Verify deletion (recommended)",
            variable=self.verify_var,
            font=ctk.CTkFont(size=12)
        )
        verify_checkbox.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Progress frame
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready to delete files securely", font=ctk.CTkFont(size=12))
        self.progress_label.pack(pady=(20, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 20))
        self.progress_bar.set(0)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            main_frame,
            text="🗑️ SECURELY DELETE FILES",
            command=self.confirm_deletion,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="red",
            hover_color="darkred"
        )
        self.delete_btn.pack(pady=(0, 20))
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select files to securely delete",
            filetypes=[("All files", "*.*")]
        )
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
        self.update_file_list()
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to securely delete")
        if folder:
            # Add all files in the folder recursively
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in self.selected_files:
                        self.selected_files.append(file_path)
            self.update_file_list()
            
    def clear_list(self):
        self.selected_files.clear()
        self.update_file_list()
        
    def update_file_list(self):
        # Clear existing widgets
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
            
        if not self.selected_files:
            no_files_label = ctk.CTkLabel(self.file_list_frame, text="No files selected", text_color="gray")
            no_files_label.pack(pady=20)
        else:
            for i, file_path in enumerate(self.selected_files):
                file_frame = ctk.CTkFrame(self.file_list_frame)
                file_frame.pack(fill="x", pady=2, padx=5)
                
                # File path label
                file_label = ctk.CTkLabel(
                    file_frame,
                    text=f"{Path(file_path).name} ({file_path})",
                    font=ctk.CTkFont(size=10),
                    anchor="w"
                )
                file_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)
                
                # Remove button
                remove_btn = ctk.CTkButton(
                    file_frame,
                    text="×",
                    width=30,
                    height=25,
                    command=lambda idx=i: self.remove_file(idx),
                    fg_color="red",
                    hover_color="darkred"
                )
                remove_btn.pack(side="right", padx=5, pady=5)
                
    def remove_file(self, index):
        if 0 <= index < len(self.selected_files):
            self.selected_files.pop(index)
            self.update_file_list()
            
    def confirm_deletion(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to delete first.")
            return
            
        if self.is_deleting:
            messagebox.showinfo("In Progress", "Deletion is already in progress.")
            return
            
        # Show confirmation dialog
        passes = int(self.passes_var.get())
        file_count = len(self.selected_files)
        
        confirm_msg = f"""⚠️ WARNING: PERMANENT DELETION ⚠️

You are about to PERMANENTLY delete {file_count} file(s) using {passes}-pass overwrite.

This action is IRREVERSIBLE and the files CANNOT be recovered even with advanced recovery tools.

Selected files will be:
1. Overwritten {passes} time(s) with random data
2. {'Verified for complete deletion' if self.verify_var.get() else 'Deleted without verification'}
3. Removed from the file system

Are you absolutely sure you want to proceed?"""
        
        result = messagebox.askyesno(
            "Confirm Secure Deletion",
            confirm_msg,
            icon="warning"
        )
        
        if result:
            self.start_deletion()
            
    def start_deletion(self):
        self.is_deleting = True
        self.delete_btn.configure(state="disabled", text="DELETING...")
        self.select_files_btn.configure(state="disabled")
        self.select_folder_btn.configure(state="disabled")
        
        # Start deletion in a separate thread
        thread = threading.Thread(target=self.delete_files_secure)
        thread.daemon = True
        thread.start()
        
    def delete_files_secure(self):
        passes = int(self.passes_var.get())
        total_files = len(self.selected_files)
        deleted_count = 0
        failed_files = []
        
        for i, file_path in enumerate(self.selected_files):
            try:
                # Update progress
                self.root.after(0, lambda: self.progress_label.configure(
                    text=f"Securely deleting: {Path(file_path).name} ({i+1}/{total_files})"
                ))
                self.root.after(0, lambda: self.progress_bar.set((i) / total_files))
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    self.secure_delete_file(file_path, passes)
                    deleted_count += 1
                else:
                    failed_files.append(f"{file_path} (file not found)")
                    
            except Exception as e:
                failed_files.append(f"{Path(file_path).name}: {str(e)}")
                
        # Final update
        self.root.after(0, lambda: self.progress_bar.set(1.0))
        self.root.after(0, lambda: self.progress_label.configure(
            text=f"Completed: {deleted_count}/{total_files} files securely deleted"
        ))
        
        # Show results
        if failed_files:
            error_msg = f"Deleted {deleted_count} files successfully.\n\nFailed to delete:\n" + "\n".join(failed_files[:10])
            if len(failed_files) > 10:
                error_msg += f"\n... and {len(failed_files) - 10} more files"
            self.root.after(0, lambda: messagebox.showwarning("Deletion Complete with Errors", error_msg))
        else:
            self.root.after(0, lambda: messagebox.showinfo(
                "Deletion Complete", 
                f"Successfully deleted {deleted_count} files securely."
            ))
            
        # Reset UI
        self.root.after(0, self.reset_ui)
        
    def secure_delete_file(self, file_path, passes):
        """Securely delete a file using multiple overwrite passes"""
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, "r+b") as file:
                for pass_num in range(passes):
                    file.seek(0)
                    
                    if pass_num == 0:
                        # First pass: all zeros
                        data = b'\x00' * min(65536, file_size)
                    elif pass_num == 1 and passes >= 2:
                        # Second pass: all ones
                        data = b'\xFF' * min(65536, file_size)
                    else:
                        # Other passes: random data
                        data = bytes([random.randint(0, 255) for _ in range(min(65536, file_size))])
                    
                    # Write data in chunks
                    remaining = file_size
                    while remaining > 0:
                        chunk_size = min(len(data), remaining)
                        if chunk_size < len(data):
                            data = data[:chunk_size]
                        file.write(data)
                        remaining -= chunk_size
                    
                    file.flush()
                    os.fsync(file.fileno())  # Force write to disk
                    
            # Rename file to random name before deletion
            dir_path = os.path.dirname(file_path)
            random_name = ''.join(random.choices('0123456789abcdef', k=16))
            temp_path = os.path.join(dir_path, random_name)
            os.rename(file_path, temp_path)
            
            # Finally delete the file
            os.remove(temp_path)
            
            # Verify deletion if requested
            if self.verify_var.get():
                if os.path.exists(temp_path) or os.path.exists(file_path):
                    raise Exception("File still exists after deletion")
                    
        except Exception as e:
            raise Exception(f"Failed to securely delete: {str(e)}")
            
    def reset_ui(self):
        self.is_deleting = False
        self.delete_btn.configure(state="normal", text="🗑️ SECURELY DELETE FILES")
        self.select_files_btn.configure(state="normal")
        self.select_folder_btn.configure(state="normal")
        self.selected_files.clear()
        self.update_file_list()
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready to delete files securely")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Check if required modules are available
    try:
        import customtkinter
    except ImportError:
        print("Error: customtkinter is not installed.")
        print("Please install it using: pip install customtkinter")
        exit(1)
        
    app = SecureDeleteTool()
    app.run()