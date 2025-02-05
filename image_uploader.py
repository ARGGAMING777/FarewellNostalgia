import os
import time
import json
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageUploadHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folder, json_file):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.json_file = json_file
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            
    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.lower().endswith(self.supported_formats):
            try:
                # Get the filename
                filename = os.path.basename(event.src_path)
                destination_path = os.path.join(self.destination_folder, filename)
                
                # Copy file to destination
                shutil.copy2(event.src_path, destination_path)
                
                # Update JSON file
                self.update_json(f"images/{filename}")
                print(f"Uploaded: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    def update_json(self, new_image_path):
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r') as f:
                    images = json.load(f)
            else:
                images = []
            
            if new_image_path not in images:
                images.append(new_image_path)
                
            with open(self.json_file, 'w') as f:
                json.dump(images, f, indent=4)
                
        except Exception as e:
            print(f"Error updating JSON: {str(e)}")

def start_watching(upload_folder):
    # Setup paths
    destination = "images"
    json_file = "images.json"
    
    # Create handler and observer
    event_handler = ImageUploadHandler(upload_folder, destination, json_file)
    observer = Observer()
    observer.schedule(event_handler, upload_folder, recursive=False)
    observer.start()
    
    print(f"Watching folder: {upload_folder}")
    print("To stop watching, press Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching folder")
    
    observer.join()

if __name__ == "__main__":
    # Replace with your upload folder path
    UPLOAD_FOLDER = r"C:\Users\aayus\Downloads\Telegram Desktop\v1\v1\Photos"
    start_watching(UPLOAD_FOLDER)