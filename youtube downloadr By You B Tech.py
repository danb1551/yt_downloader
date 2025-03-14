import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
import threading
import os
from datetime import datetime

download_history = []  # List to store download history
#     https://www.youtube.com/watch?v=L-03Rc4j_9g
#     https://www.youtube.com/watch?v=XM3bV42rkGw

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    download_button.config(state=tk.DISABLED)
    audio_button.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    status_label.config(text="Starting download...")

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        progress_bar['value'] = percentage_of_completion
        status_label.config(text=f"Downloading... {int(percentage_of_completion)}%")

    def on_complete(stream, file_path):
        status_label.config(text="Downloaded")
        root.after(1000, lambda: status_label.config(text="Download complete!"))

        # Reset fields after 5 seconds
        root.after(5000, reset_fields)
        download_button.config(state=tk.NORMAL)
        audio_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {file_path}")
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        download_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        download_history.append({'file_name': file_name, 'file_size': file_size, 'download_time': download_time})  # Add download information to history
        update_history_listbox()  # Update download history listbox

    def start_download():
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            stream = yt.streams.get_highest_resolution()
            download_path = filedialog.askdirectory()
            if download_path:
                file_path = stream.download(output_path=download_path)
                url_entry.delete(0, tk.END)  # Clear URL entry after successful download
                on_complete(stream, file_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            download_button.config(state=tk.NORMAL)
            audio_button.config(state=tk.NORMAL)
            status_label.config(text="")

    threading.Thread(target=start_download).start()

def download_audio():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    download_button.config(state=tk.DISABLED)
    audio_button.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    status_label.config(text="Starting download...")

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        progress_bar['value'] = percentage_of_completion
        status_label.config(text=f"Downloading... {int(percentage_of_completion)}%")

    def on_complete(stream, file_path):
        status_label.config(text="Downloaded")
        root.after(1000, lambda: status_label.config(text="Download complete!"))

        # Reset fields after 5 seconds
        root.after(5000, reset_fields)
        download_button.config(state=tk.NORMAL)
        audio_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success", f"Audio downloaded successfully!\nSaved to: {file_path}")
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        download_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        download_history.append({'file_name': file_name, 'file_size': file_size, 'download_time': download_time})  # Add download information to history
        update_history_listbox()  # Update download history listbox

    def start_download():
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            stream = yt.streams.filter(only_audio=True).first()
            download_path = filedialog.askdirectory()
            if download_path:
                file_path = stream.download(output_path=download_path)
                url_entry.delete(0, tk.END)  # Clear URL entry after successful download
                on_complete(stream, file_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            download_button.config(state=tk.NORMAL)
            audio_button.config(state=tk.NORMAL)
            status_label.config(text="")

    threading.Thread(target=start_download).start()

def reset_fields():
    progress_bar['value'] = 0
    status_label.config(text="")

def paste_clipboard():
    try:
        clipboard_content = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, clipboard_content)
    except tk.TclError:
        messagebox.showerror("Error", "No content in clipboard")

def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for item in download_history:
        history_listbox.insert(tk.END, f"{item['file_name']} - Size: {item['file_size']} bytes - Downloaded at: {item['download_time']}")

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("600x400")  # Set window size

# URL entry
url_label = tk.Label(root, text="Enter YouTube URL:", font=('Arial', 12))
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50, font=('Arial', 12))
url_entry.pack(pady=5)

# Paste button
paste_button = tk.Button(root, text="Paste", command=paste_clipboard, font=('Arial', 10))
paste_button.pack(pady=5)

# Download Video button
download_button = tk.Button(root, text="Download Video", command=download_video, bg="blue", fg="white", font=('Arial', 10))  # Set background and foreground color
download_button.pack(pady=10)

# Download Audio button
audio_button = tk.Button(root, text="Download Audio", command=download_audio, bg="green", fg="white", font=('Arial', 10))  # Set background and foreground color
audio_button.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", font=('Arial', 12))
status_label.pack(pady=5)

# Download history listbox
history_frame = ttk.Frame(root)
history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

history_label = tk.Label(history_frame, text="Download History:", font=('Arial', 12))
history_label.pack()

history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL)
history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_listbox = tk.Listbox(history_frame, yscrollcommand=history_scrollbar.set, width=70, font=('Arial', 10))
history_listbox.pack(pady=5)

history_scrollbar.config(command=history_listbox.yview)

# Update download history listbox initially
update_history_listbox()

root.mainloop()