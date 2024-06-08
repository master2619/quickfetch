Quickfetch is a simple, multi-platform system information tool inspired by Neofetch, written in Python. It provides detailed information about your operating system, kernel, architecture, CPU, GPU, memory, uptime, and installed package managers. Additionally, it includes a colorful strip for enhanced visual appeal.
Features

    Displays user, hostname, OS, kernel, architecture, CPU, GPU, memory, and uptime information.
    Detects and lists installed package managers along with the number of installed packages.
    Compatible with Linux and other platforms.
    Includes a colorful strip at the bottom of the output.

Sample Output

shell

User: user@hostname
OS: Zorin OS 17.1
Kernel: 6.9.3-x64v3-xanmod1
Architecture: x86_64
CPU: AMD Ryzen 3 3250U with Radeon Graphics (4 cores)
GPU: AMD Radeon Graphics
Memory: 2.15GiB / 21.45GiB
Uptime: 0:11:01
Apt: 1250 packages
Snap: 30 packages
Flatpak: 20 packages
████████████████████████████████████████████████████████████████████

Dependencies

    Python 3
    psutil
    platform
    cpuinfo
    GPUtil
    distro
    py3nvml
    lshw

Installation
Installing from Source

    Clone the repository:

    bash

git clone https://github.com/yourusername/quickfetch.git
cd quickfetch

Install the dependencies:

bash

pip install psutil py-cpuinfo gputil py3nvml distro
sudo apt install lshw

Run the script:

bash

    python3 quickfetch.py

Contributing

Feel free to submit issues or pull requests if you have any improvements or suggestions.
License

This project is licensed under the GPL-3.0 License.
