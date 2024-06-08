QuickFetch is a Linux-only system information tool written in Python, designed to display useful system details in a concise and visually appealing way. It provides information such as the operating system, kernel, architecture, CPU, GPU, memory usage, uptime, and package manager statistics.
Features

    Displays user information
    Shows OS and kernel version
    Lists architecture and CPU details
    Shows GPU information (integrated and dedicated)
    Displays memory usage
    Shows system uptime
    Lists package counts from common package managers (dpkg, apt, snap, flatpak, and universal package managers)
    And more!

Installation and Dependencies :-

Easy Method (Single Command) :-

```bash
sudo apt install curl && curl -sSL https://github.com/master2619/quickfetch/releases/download/release-2/installer.sh | sudo sh
```

Manual Compile and Install method :-

QuickFetch requires the following Python libraries:

    psutil
    distro
    colorama
    GPUtil

Install the dependencies using pip:

pip3 install psutil distro colorama GPUtil

Compiling from Source

To compile QuickFetch into a standalone executable using PyInstaller, follow these steps:

pip3 install pyinstaller

Ensure PyInstaller is in Your PATH:

If pyinstaller command is not found after installation, you may need to add the local installation directory to your PATH. Find the installation location:

pip3 show pyinstaller

Look for the Location line in the output and add the bin directory within this location to your PATH. For example:

export PATH=$PATH:/home/$USER/.local/bin

To make this change permanent, add the above line to your ~/.profile or ~/.bashrc or ~/.bash_profile file and reload it:

echo 'export PATH=$PATH:/home/$USER/.local/bin' >> ~/.bashrc

source ~/.bashrc

Compile the Script:

Navigate to the directory containing quickfetch.py and run:

    pyinstaller --onefile quickfetch.py

    The compiled executable will be located in the dist directory.

Move the compiled binary to /usr/bin folder for permanent installation :-

sudo mv /home/$USER/quickfetch/dist/quickfetch /usr/bin/quickfetch

Usage

Simply run the quickfetch executable from your terminal:

./quickfetch

You will see output similar to the following:

User: deepesh@HP-Linux-Laptop
OS: Zorin OS 17.1
Kernel: 6.9.3-x64v3-xanmod1
Architecture: x86_64
CPU: AMD Ryzen 3 3250U with Radeon Graphics (4 cores)
GPU: Picasso/Raven 2 [Radeon Vega Series / Radeon Vega Mobile Series]
Memory: 2.63GiB / 21.45GiB
Uptime: 0:25:16
Dpkg: 2812 packages
Apt: 2808 packages
Snap: 7 packages
Flatpak: 39 packages

To make this quickfetch binary you either compiled or downloaded accesible from anywhere in the terminal, follow these steps:-

Add the parent directory of the binary file to your ~/.bashrc or ~/.profile file by running :-

echo 'export PATH=$PATH:/home/$USER/Downloads/' >> ~/.bashrc

License

This project is licensed under the GPL 3.0 License. See the LICENSE file for details.
Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
Issues

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.
Acknowledgements :-

    Inspired by Neofetch
    Uses psutil for system information
    Uses distro for Linux distribution detection
    Uses GPUtil for GPU information
    Uses colorama for colored terminal output
