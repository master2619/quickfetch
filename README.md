# **QuickFetch**  

QuickFetch is a lightweight system information tool designed for Linux systems. It provides concise and visually appealing details about your system's configuration and usage. With QuickFetch, you can quickly access essential information such as the operating system, kernel version, hardware architecture, CPU and GPU specifications, memory usage, uptime, and package manager statistics.  

## **Features**  
✔ Displays essential system information (OS, kernel, CPU, GPU, memory, uptime, etc.)  
✔ Supports multiple display resolutions and desktop environments  
✔ Detects and displays disk usage across multiple partitions  
✔ Shows battery status and local IP  
✔ Package Manager Detection (Only on Debian-based systems: `dpkg`, `apt`, `snap`, `flatpak`)  
✔ Works on all major Linux distributions  
✔ Lightweight and easy to install  

### **Sample Output**  
```
User: hypr@HP-Linux
OS: Manjaro Linux
Kernel: 6.12.12-2-MANJARO
Architecture: x86_64
CPU: AMD Ryzen 3 3250U with Radeon Graphics (4 cores)
GPU: No GPU found
Memory: 2.81GiB / 21.45GiB
Swap: 0.00GiB / 23.59GiB
Uptime: 3:01:59
Resolution: 1920x1080
DE: Hyprland
WM: Wayland
WM Theme: Unknown
Theme: Rose-Pine
Icons: Tela-circle-pink
Terminal: truecolor
Terminal Font: CaskaydiaCove Nerd Font Mono 9
System Font: Unknown
Disk (/): 80.18GiB / 907.62GiB
Disk (/home): 80.18GiB / 907.62GiB
Disk (/var/cache): 80.18GiB / 907.62GiB
Disk (/var/log): 80.18GiB / 907.62GiB
Disk (/boot/efi): 0.00GiB / 0.29GiB
Disk (/run/media/deepesh/DATA): 271.19GiB / 931.50GiB
Local IP: 192.168.1.16
Battery: 24.196787148594378% [Discharging]
Locale: en_IN
```
> **Note:** Debian-based Linux systems may also display package manager stats.
---

## **Installation**  

### **Easy Installation (Debian-Based Distros)**  
For Debian-based distributions (Ubuntu, Zorin OS, Pop!_OS, Linux Mint, etc.), you can install QuickFetch using a single command:  
```bash
sudo apt install curl && curl -sSL https://github.com/master2619/quickfetch/releases/download/release-3/installer.sh | sudo sh
```
### **Easy Installation (Fedora-based Distros)**
For Fedora-based Linux distributions.
```bash
sudo dnf install curl -y && curl -sSL https://github.com/master2619/quickfetch/releases/download/release-3/installer.sh | sudo sh
```
### **Easy Installation (Arch-Based Distros)**
For Arch-based distributions like Manjaro, Arco Linux, etc.
```bash
sudo pacman -S curl && curl -sSL https://github.com/master2619/quickfetch/releases/download/release-3/installer.sh | sudo sh
```

> **Note:** If you are using other Linux distributions or on an alternate architecture, follow the **manual installation** steps below.

---

### **Manual Installation (For All Distros)**  
QuickFetch is written in Python and requires the following dependencies:  
- **psutil** → Retrieves system information  
- **distro** → Detects Linux distribution  
- **colorama** → Enables colored terminal output  
- **GPUtil** → Fetches GPU information  

#### **Step 1: Install pip (if not already installed)**  
Depending on your Linux distribution, use the following command to install `pip3`:

- **Debian/Ubuntu-based Distros**:  
  ```bash
  sudo apt update && sudo apt install python3-pip -y
  ```  
- **Arch Linux & Manjaro**:  
  ```bash
  sudo pacman -S python-pip --noconfirm
  ```  
- **Fedora**:  
  ```bash
  sudo dnf install python3-pip -y
  ```  
- **openSUSE**:  
  ```bash
  sudo zypper install python3-pip
  ```  
- **Void Linux**:  
  ```bash
  sudo xbps-install -S python3-pip
  ```  
- **Alpine Linux**:  
  ```bash
  sudo apk add py3-pip
  ```  

#### **Step 2: Install Dependencies**  
```bash
pip3 install psutil distro colorama GPUtil py-cpuinfo --break-system-packages
```

#### **Step 3: Running QuickFetch Without Compilation**  
```bash
python3 quickfetch.py
```

---

### **Compiling QuickFetch (For Standalone Usage)**  
#### **Step 1: Install PyInstaller**  
```bash
pip3 install pyinstaller --break-system-packages
```
#### **Step 2: Add Pyinstaller to Console PATH**
```bash
export PATH=$PATH:/home/$USER/.local/bin
```
#### **Step 3: Compile QuickFetch**  
```bash
pyinstaller --onefile quickfetch.py
```
#### **Step 4: Move the Compiled Binary for Global Access**  
```bash
sudo mv /home/$USER/quickfetch/dist/quickfetch /usr/bin/quickfetch
```

---

## **Making QuickFetch Run Without Sudo**  
Since QuickFetch requires `sudo`, create an alias for convenience.  

### **Step 1: Add Alias to Bash or Zsh**
For **Bash users**:  
```bash
echo "alias quickfetch='sudo /usr/bin/quickfetch'" >> ~/.bashrc
source ~/.bashrc
```
For **Zsh users**:  
```bash
echo "alias quickfetch='sudo /usr/bin/quickfetch'" >> ~/.zshrc
source ~/.zshrc
```
This ensures `quickfetch` runs with `sudo` automatically.

---

## **Usage**  
```bash
quickfetch
```

---

## **License**  
GPL 3.0 License. See the LICENSE file for details.  

---

## **Contributing**  
Fork the repository and create a pull request with your changes.  

---

## **Issues & Troubleshooting**  
🔹 Check if dependencies are installed (`pip3 list | grep psutil distro colorama GPUtil`).  
🔹 Ensure the binary is in `/usr/bin/`.  
🔹 Open an **issue** on GitHub for help.  

---

## **Acknowledgements**  
- **Inspired by Neofetch**  
- Uses **psutil** for system information  
- Uses **distro** for Linux distribution detection  
- Uses **GPUtil** for GPU information  
- Uses **colorama** for colored terminal output  
