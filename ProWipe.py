import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import threading
import time
import platform
from pathlib import Path

class SecureDeleteTool:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("ProWipe - Advanced Secure File Deletion Tool")
        self.root.geometry("900x750")
        self.root.minsize(700, 600)
        
        # Variables
        self.selected_files = []
        self.is_deleting = False
        self.drive_types = {}  # Cache for drive type detection
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="ProWipe - Advanced Secure File Deletion",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Military-grade secure deletion with intelligent drive detection",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # File selection frame (fixed size, no expand)
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=20, pady=(0, 15))
        
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
        
        # Scrollable frame for file list (fixed height)
        self.file_list_frame = ctk.CTkScrollableFrame(file_frame, height=120)
        self.file_list_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Drive detection info frame (with scrollable content)
        self.drive_info_frame = ctk.CTkFrame(main_frame)
        self.drive_info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        drive_info_label = ctk.CTkLabel(
            self.drive_info_frame, 
            text="📊 Drive Analysis:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        drive_info_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Scrollable frame for drive info
        drive_info_scroll = ctk.CTkScrollableFrame(self.drive_info_frame, height=80)
        drive_info_scroll.pack(fill="x", padx=20, pady=(0, 15))
        
        self.drive_info_text = ctk.CTkLabel(
            drive_info_scroll,
            text="No files selected. Drive analysis will appear here.",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left",
            anchor="w"
        )
        self.drive_info_text.pack(fill="x", padx=10, pady=5)
        
        # Options frame (compact)
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        options_label = ctk.CTkLabel(options_frame, text="Deletion Options:", font=ctk.CTkFont(size=14, weight="bold"))
        options_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Overwrite passes
        passes_frame = ctk.CTkFrame(options_frame)
        passes_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(passes_frame, text="Overwrite Passes:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(20, 10), pady=10)
        
        self.passes_var = ctk.StringVar(value="3")
        self.passes_menu = ctk.CTkOptionMenu(
            passes_frame,
            values=["1", "3", "7", "35"],
            variable=self.passes_var,
            width=80,
            command=self.on_passes_changed
        )
        self.passes_menu.pack(side="left", padx=(0, 20), pady=10)
        
        # Info label
        self.info_label = ctk.CTkLabel(
            passes_frame, 
            text="• 1 pass: Quick deletion\n• 3 passes: DoD standard (recommended)\n• 7 passes: High security (HDD only)\n• 35 passes: Gutmann method (HDD only)",
            font=ctk.CTkFont(size=10),
            justify="left"
        )
        self.info_label.pack(side="left", padx=(20, 0), pady=10)
        
        # Verify deletion checkbox
        self.verify_var = ctk.BooleanVar(value=True)
        verify_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Verify deletion (recommended)",
            variable=self.verify_var,
            font=ctk.CTkFont(size=12)
        )
        verify_checkbox.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Progress frame (compact)
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready to delete files securely", font=ctk.CTkFont(size=12))
        self.progress_label.pack(pady=(15, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
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
        
    def detect_drive_type(self, file_path):
        """Detect if the drive is SSD, HDD, or USB/Flash"""
        try:
            if platform.system() != 'Windows':
                return "Unknown"
            
            # Get drive letter
            drive = os.path.splitdrive(file_path)[0]
            if not drive:
                return "Unknown"
                
            # Check cache first
            if drive in self.drive_types:
                return self.drive_types[drive]
            
            # Try to detect drive type using Windows methods
            drive_type = self.detect_windows_drive_type(drive)
            self.drive_types[drive] = drive_type
            return drive_type
            
        except Exception as e:
            return "Unknown"
    
    def detect_windows_drive_type(self, drive):
        """Detect drive type on Windows using multiple methods"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Method 1: Check if it's a removable drive (USB flash drive)
            drive_type_code = ctypes.windll.kernel32.GetDriveTypeW(drive + "\\")
            if drive_type_code == 2:  # DRIVE_REMOVABLE
                return "USB Flash Drive"
            
            # Method 2: Use WMI for more detailed detection
            try:
                import subprocess
                import json
                
                # Run PowerShell command to get disk info
                ps_command = f"""
                Get-PhysicalDisk | Where-Object {{$_.DeviceID -ne $null}} | Select-Object MediaType, BusType | ConvertTo-Json
                """
                
                result = subprocess.run(
                    ["powershell", "-Command", ps_command],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                
                if result.returncode == 0 and result.stdout:
                    disks = json.loads(result.stdout)
                    if not isinstance(disks, list):
                        disks = [disks]
                    
                    for disk in disks:
                        media_type = disk.get('MediaType', '').upper()
                        bus_type = disk.get('BusType', '').upper()
                        
                        # Check for USB
                        if 'USB' in bus_type or bus_type == '7':
                            return "USB Flash Drive"
                        
                        # Check for SSD
                        if 'SSD' in media_type or media_type == '4':
                            return "SSD"
                        
                        # Check for HDD
                        if 'HDD' in media_type or media_type == '3':
                            return "HDD"
                
            except Exception:
                pass
            
            # Fallback: Assume it's HDD if fixed and not removable
            if drive_type_code == 3:  # DRIVE_FIXED
                return "HDD/SSD"
                
            return "Unknown"
            
        except Exception:
            return "Unknown"
    
    def analyze_selected_drives(self):
        """Analyze all drives containing selected files"""
        if not self.selected_files:
            self.drive_info_text.configure(
                text="No files selected. Drive analysis will appear here.",
                text_color="gray"
            )
            return
        
        # Group files by drive and type
        drive_analysis = {}
        
        for file_path in self.selected_files:
            drive = os.path.splitdrive(file_path)[0]
            if drive:
                drive_type = self.detect_drive_type(file_path)
                
                if drive not in drive_analysis:
                    drive_analysis[drive] = {
                        'type': drive_type,
                        'count': 0
                    }
                drive_analysis[drive]['count'] += 1
        
        # Build info text
        info_lines = []
        has_flash = False
        has_hdd = False
        
        for drive, info in sorted(drive_analysis.items()):
            icon = "💾"
            warning = ""
            
            if "USB" in info['type'] or "Flash" in info['type']:
                icon = "🔌"
                has_flash = True
                warning = " ⚠️ Flash storage detected!"
            elif "SSD" in info['type']:
                icon = "💿"
                has_flash = True
                warning = " ⚠️ SSD detected!"
            elif "HDD" in info['type']:
                icon = "💽"
                has_hdd = True
            
            info_lines.append(
                f"{icon} Drive {drive}\\ - {info['type']} - {info['count']} file(s){warning}"
            )
        
        # Add recommendations
        info_lines.append("")
        if has_flash:
            info_lines.append("⚠️ FLASH STORAGE DETECTED (SSD/USB):")
            info_lines.append("• Multi-pass overwrites are INEFFECTIVE on flash storage")
            info_lines.append("• Recommended: Use 1 pass only (more passes don't help)")
            info_lines.append("• Reason: Wear leveling prevents true overwriting")
            info_lines.append("• For complete security: Use manufacturer's secure erase tool")
        
        if has_hdd:
            info_lines.append("✅ TRADITIONAL HDD DETECTED:")
            info_lines.append("• Multi-pass overwrites are EFFECTIVE")
            info_lines.append("• Recommended: 3 passes (DoD standard)")
            info_lines.append("• 7-35 passes available for higher security needs")
        
        self.drive_info_text.configure(
            text="\n".join(info_lines),
            text_color="white"
        )
        
        # Auto-adjust recommendation for passes
        if has_flash and not has_hdd:
            if self.passes_var.get() != "1":
                self.show_flash_warning()
    
    def show_flash_warning(self):
        """Show warning when flash storage is detected with multi-pass selected"""
        messagebox.showinfo(
            "Flash Storage Detected",
            "⚠️ Flash storage (SSD/USB) detected!\n\n"
            "Multi-pass overwrites (3, 7, or 35 passes) are INEFFECTIVE on flash storage "
            "due to wear leveling and controller optimizations.\n\n"
            "Recommendation: Use 1 pass only.\n\n"
            "For complete security on SSDs, use:\n"
            "• Manufacturer's secure erase tool\n"
            "• ATA Secure Erase command\n"
            "• Full disk encryption + crypto erase\n"
            "• Physical destruction"
        )
    
    def on_passes_changed(self, choice):
        """Handle passes selection change"""
        # Re-analyze drives to show appropriate warnings
        self.analyze_selected_drives()
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select files to securely delete",
            filetypes=[("All files", "*.*")]
        )
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
        self.update_file_list()
        self.analyze_selected_drives()
        
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
            self.analyze_selected_drives()
            
    def clear_list(self):
        self.selected_files.clear()
        self.update_file_list()
        self.analyze_selected_drives()
        
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
                
                # Detect drive type for icon
                drive_type = self.detect_drive_type(file_path)
                icon = "💾"
                if "USB" in drive_type or "Flash" in drive_type:
                    icon = "🔌"
                elif "SSD" in drive_type:
                    icon = "💿"
                elif "HDD" in drive_type:
                    icon = "💽"
                
                # File path label
                file_label = ctk.CTkLabel(
                    file_frame,
                    text=f"{icon} {Path(file_path).name} ({file_path})",
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
            self.analyze_selected_drives()
            
    def confirm_deletion(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to delete first.")
            return
            
        if self.is_deleting:
            messagebox.showinfo("In Progress", "Deletion is already in progress.")
            return
        
        # Check for flash storage with multi-pass
        has_flash = False
        for file_path in self.selected_files:
            drive_type = self.detect_drive_type(file_path)
            if "USB" in drive_type or "Flash" in drive_type or "SSD" in drive_type:
                has_flash = True
                break
        
        passes = int(self.passes_var.get())
        
        # Show warning if using multi-pass on flash storage
        flash_warning = ""
        if has_flash and passes > 1:
            flash_warning = "\n\n⚠️ WARNING: Flash storage (SSD/USB) detected!\nMulti-pass overwrites are NOT effective on flash storage.\nConsider using 1 pass instead.\n"
            
        # Show confirmation dialog
        file_count = len(self.selected_files)
        
        confirm_msg = f"""⚠️ WARNING: PERMANENT DELETION ⚠️

You are about to PERMANENTLY delete {file_count} file(s) using {passes}-pass overwrite.

This action is IRREVERSIBLE and the files CANNOT be recovered even with advanced recovery tools.

Selected files will be:
1. Overwritten {passes} time(s) with random data
2. {'Verified for complete deletion' if self.verify_var.get() else 'Deleted without verification'}
3. Removed from the file system{flash_warning}

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
        self.analyze_selected_drives()
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
