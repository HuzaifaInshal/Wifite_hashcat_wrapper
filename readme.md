
# Wifite + Hashcat Automation

This Python script automates the process of capturing WPA handshakes using Wifite, converting .cap files to .hc22000 format, and then running a Hashcat attack using a specified wordlist. It supports flexible wordlist selection from a local directory and performs automatic cleanup of .hc22000 files after the process is done.




## Features

- **Capture WPA Handshake:** Uses Wifite to perform a WPA handshake attack.
- **Convert .cap to .hc22000:** Converts `.cap` files into `.hc22000` format using `hcxpcapngtool`.
- **Select Wordlist:** Prompts the user to choose a wordlist from the wordlists/ directory for Hashcat.
- **Hashcat Cracking:** Runs Hashcat using the selected wordlist and device.
- **Cleanup:** Deletes files after the attack is complete to avoid future mismatches or file collisions.


## Requirements

- **Python 3.x**
- **Wifite:** [Wifite GitHub](https://github.com/derv82/wifite)
- **hcxpcapngtool:** [hcxpcapngtool GitHub](https://github.com/ZerBea/hcxtools)
- **Hashcat:** [Hashcat Official Website](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://hashcat.net/hashcat/&ved=2ahUKEwiVuJrcoauNAxW4h_0HHUdWI-gQFnoECBEQAQ&usg=AOvVaw3K-lSmnFyDtqcjypGTmOVd)

Ensure you have all the required dependencies installed. For example, you can install Hashcat using:

```
sudo apt install hashcat
```


## Usage

### 1. Download Wordlists
The script allows you to choose from local wordlists. Two popular wordlists can be downloaded using the following commands:

**RockYou.txt:**
To download the rockyou.txt wordlist and store it in the `wordlists/` directory, use the following bash commands:
```
# if wordlist dir not present then move into it
mkdir wordlists && cd wordlists

# execute the main command
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

# get out of the folder
cd ..
```

**General List (Paklist):**
To download the general-list.zip and unzip it to `general-list.txt`, run the following bash commands:

```
# if wordlist dir not present then create and move into it
mkdir wordlists && cd wordlists

# main commands
wget https://github.com/usama-365/paklist/raw/refs/heads/master/general-list.zip
unzip general-list.zip

# get out of the wordlist folder
cd ..
```

### 2. Running the Script
Once you've downloaded the necessary wordlists, you can run the script as follows:
```
sudo python3 script.py
```

The script will perform the following steps:

- **Wifite:** Start a WPA handshake attack using Wifite.
- **Conversion:** Convert `.cap` files to `.hc22000` format using hcxpcapngtool.
- **Hashcat:** Run Hashcat with the selected wordlist and device.
- **Cleanup:** Remove the files after the cracking process if asked.

## Problems
In case the hashcat is not running because of potfile record, you can find the location of potfile with:
```
sudo find / | grep "hashcat.potfile"
```
and remove the potfile.

## Customization
- **Wordlist Directory:** The wordlists should be placed in the `wordlists/` directory. The script will automatically prompt you to choose a wordlist by number.

- **Device Selection:** The script automatically detects your available Hashcat devices. You'll be prompted to choose the device you want to use for cracking.
