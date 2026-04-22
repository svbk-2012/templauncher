import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
import threading
import os
import shutil
import time
import json
from pathlib import Path
import psutil
import winreg
from datetime import datetime

class LauncherWrapper:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher Wrapper - Download & Save Apps")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Create downloads directory
        self.downloads_dir = Path.home() / "Downloads" / "LauncherWrapper"
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Current launcher info
        self.current_launcher = None
        self.process = None
        self.monitoring = False
        self.downloaded_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_font = tkFont.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(self.root, text="Launcher Wrapper", 
                               font=title_font, bg='#2b2b2b', fg='white')
        title_label.pack(pady=20)
        
        # Drag and Drop Area
        self.drop_frame = tk.Frame(self.root, bg='#3c3c3c', relief='ridge', bd=2)
        self.drop_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        self.drop_label = tk.Label(self.drop_frame, 
                                  text="Drag and drop launcher files here\n(.exe, .msi, .zip, etc.)",
                                  font=("Arial", 14), bg='#3c3c3c', fg='#cccccc')
        self.drop_label.pack(expand=True)
        
        # Register drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                     font=("Arial", 10), bg='#2b2b2b', fg='#00ff00')
        self.status_label.pack(side='left')
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=5)
        
        # Buttons Frame
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=10)
        
        self.launch_btn = tk.Button(button_frame, text="Launch Download", 
                                    command=self.launch_downloader,
                                    state='disabled', bg='#4CAF50', fg='white')
        self.launch_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop", 
                                  command=self.stop_process,
                                  state='disabled', bg='#f44336', fg='white')
        self.stop_btn.pack(side='left', padx=5)
        
        self.open_folder_btn = tk.Button(button_frame, text="Open Downloads Folder", 
                                        command=self.open_downloads_folder,
                                        bg='#2196F3', fg='white')
        self.open_folder_btn.pack(side='left', padx=5)
        
        # Downloads List
        list_frame = tk.Frame(self.root, bg='#2b2b2b')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(list_frame, text="Downloaded Applications:", 
                font=("Arial", 12, "bold"), bg='#2b2b2b', fg='white').pack(anchor='w')
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.downloads_listbox = tk.Listbox(list_frame, 
                                            yscrollcommand=scrollbar.set,
                                            bg='#3c3c3c', fg='white',
                                            selectbackground='#5a5a5a')
        self.downloads_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.downloads_listbox.yview)
        
        self.load_downloaded_apps()
        
    def on_drag_enter(self, event):
        self.drop_frame.configure(bg='#4a4a4a')
        self.drop_label.configure(text="Release to drop launcher file")
        
    def on_drag_leave(self, event):
        self.drop_frame.configure(bg='#3c3c3c')
        self.drop_label.configure(text="Drag and drop launcher files here\n(.exe, .msi, .zip, etc.)")
        
    def on_drop(self, event):
        self.drop_frame.configure(bg='#3c3c3c')
        files = self.root.tk.splitlist(event.data)
        
        if files:
            launcher_path = files[0].strip('{}')  # Remove curly braces
            if os.path.exists(launcher_path):
                self.handle_launcher_file(launcher_path)
            else:
                messagebox.showerror("Error", f"File not found: {launcher_path}")
                
    def handle_launcher_file(self, launcher_path):
        file_ext = Path(launcher_path).suffix.lower()
        supported_extensions = ['.exe', '.msi', '.zip', '.7z', '.rar']
        
        if file_ext not in supported_extensions:
            messagebox.showwarning("Warning", 
                                  f"File type {file_ext} may not be supported.\n"
                                  f"Supported types: {', '.join(supported_extensions)}")
        
        self.current_launcher = launcher_path
        launcher_name = Path(launcher_path).name
        self.drop_label.configure(text=f"Selected: {launcher_name}")
        self.launch_btn.configure(state='normal')
        self.status_label.configure(text=f"Ready to launch: {launcher_name}", fg='#00ff00')
        
    def launch_downloader(self):
        if not self.current_launcher:
            messagebox.showerror("Error", "No launcher file selected")
            return
            
        try:
            # Create temporary directory for this session
            session_dir = self.downloads_dir / f"session_{int(time.time())}"
            session_dir.mkdir(exist_ok=True)
            
            # Start monitoring for new files
            self.monitoring = True
            monitor_thread = threading.Thread(target=self.monitor_downloads, 
                                             args=(session_dir,))
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # Launch the installer
            self.status_label.configure(text="Launching downloader...", fg='#ffff00')
            self.progress.start()
            self.launch_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            
            # Run the launcher with working directory set to session folder
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.process = subprocess.Popen([self.current_launcher], 
                                           cwd=session_dir,
                                           startupinfo=startupinfo)
            
            # Wait for process to complete
            self.root.after(1000, self.check_process_status)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch downloader: {str(e)}")
            self.stop_process()
            
    def check_process_status(self):
        if self.process and self.process.poll() is None:
            # Still running
            self.root.after(1000, self.check_process_status)
        else:
            # Process completed
            self.monitoring = False
            self.progress.stop()
            self.stop_btn.configure(state='disabled')
            self.status_label.configure(text="Download completed!", fg='#00ff00')
            self.load_downloaded_apps()
            
    def monitor_downloads(self, session_dir):
        initial_files = set()
        if session_dir.exists():
            initial_files = set(session_dir.rglob('*'))
            
        while self.monitoring:
            time.sleep(2)
            
            if not session_dir.exists():
                continue
                
            current_files = set(session_dir.rglob('*'))
            new_files = current_files - initial_files
            
            for file_path in new_files:
                if file_path.is_file() and file_path.stat().st_size > 1024:  # > 1KB
                    self.root.after(0, self.new_file_detected, file_path, session_dir)
                    
            initial_files = current_files
            
    def new_file_detected(self, file_path, session_dir):
        file_size = file_path.stat().st_size
        file_name = file_path.name
        
        # Move to main downloads directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{timestamp}_{file_name}"
        destination = self.downloads_dir / new_name
        
        try:
            shutil.move(str(file_path), str(destination))
            self.downloaded_files.append({
                'name': file_name,
                'path': str(destination),
                'size': file_size,
                'timestamp': timestamp
            })
            
            self.status_label.configure(text=f"Downloaded: {file_name}", fg='#00ff00')
            self.load_downloaded_apps()
            
        except Exception as e:
            print(f"Error moving file: {e}")
            
    def stop_process(self):
        self.monitoring = False
        self.progress.stop()
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
                    
        self.process = None
        self.stop_btn.configure(state='disabled')
        self.status_label.configure(text="Stopped", fg='#ff0000')
        
    def open_downloads_folder(self):
        os.startfile(str(self.downloads_dir))
        
    def load_downloaded_apps(self):
        self.downloads_listbox.delete(0, tk.END)
        
        if self.downloads_dir.exists():
            for file_path in sorted(self.downloads_dir.glob('*'), 
                                   key=lambda x: x.stat().st_mtime, reverse=True):
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    display_text = f"{file_path.name} ({size_mb:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}"
                    self.downloads_listbox.insert(tk.END, display_text)

def main():
    root = TkinterDnD.Tk()
    app = LauncherWrapper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
