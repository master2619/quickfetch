import os
import platform
import psutil
import socket
import subprocess
from datetime import datetime
import distro
import cpuinfo
import GPUtil

def get_os_info():
    if platform.system() == "Linux":
        dist_name = distro.name(pretty=True)
        return dist_name
    else:
        return f"{platform.system()} {platform.release()}"

def get_kernel_info():
    return platform.release()

def get_arch_info():
    return platform.machine()

def get_cpu_info():
    cpu = cpuinfo.get_cpu_info()
    cpu_name = cpu['brand_raw']
    cpu_cores = psutil.cpu_count(logical=True)
    return cpu_name, cpu_cores

def get_memory_info():
    mem = psutil.virtual_memory()
    return mem.total, mem.used

def get_uptime_info():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.now()
    uptime = now - boot_time
    return str(uptime).split('.')[0]  # Remove microseconds

def get_hostname_info():
    return socket.gethostname()

def get_user_info():
    return os.getlogin()

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append(gpu.name)
    if not gpu_list:
        # Check for integrated GPUs using lshw
        try:
            output = subprocess.check_output("sudo lshw -C display 2>/dev/null", shell=True).decode()
            for line in output.split("\n"):
                if "product:" in line:
                    gpu_list.append(line.strip().split("product:")[1].strip())
        except:
            pass
    return ', '.join(gpu_list) if gpu_list else 'No GPU found'

def get_package_manager_info():
    package_managers = {
        "dpkg": "dpkg-query -f '.\n' -W 2>/dev/null | wc -l",
        "apt": "apt list --installed 2>/dev/null | wc -l",
        "rpm": "rpm -qa 2>/dev/null | wc -l",
        "pacman": "pacman -Q 2>/dev/null | wc -l",
        "dnf": "dnf list installed 2>/dev/null | wc -l",
        "snap": "snap list 2>/dev/null | wc -l",
        "flatpak": "flatpak list 2>/dev/null | wc -l"
    }
    installed_packages = {}
    for manager, command in package_managers.items():
        try:
            count = int(subprocess.check_output(command, shell=True).strip())
            if count > 0:
                installed_packages[manager] = count
        except:
            pass
    return installed_packages

def get_resolution():
    try:
        output = os.popen('xrandr').read()
        for line in output.splitlines():
            if 'connected primary' in line:
                resolution = line.split()[0]
                return resolution
    except:
        return "Unknown"

def get_desktop_environment():
    desktop_session = os.environ.get('DESKTOP_SESSION', "").lower()
    if "gnome" in desktop_session:
        return "GNOME"
    elif "kde" in desktop_session:
        return "KDE Plasma"
    elif "xfce" in desktop_session:
        return "XFCE"
    elif "lxqt" in desktop_session:
        return "LXQt"
    elif "lxde" in desktop_session:
        return "LXDE"
    elif "mate" in desktop_session:
        return "MATE"
    elif "cinnamon" in desktop_session:
        return "Cinnamon"
    elif "budgie" in desktop_session:
        return "Budgie"
    elif "pantheon" in desktop_session:
        return "Pantheon"
    else:
        return desktop_session.capitalize() if desktop_session else "Unknown"

def get_window_manager():
    window_manager = os.environ.get('XDG_SESSION_TYPE', "").lower()
    if window_manager == "wayland":
        return "Wayland"
    elif "x11" in window_manager:
        try:
            output = subprocess.check_output("wmctrl -m 2>/dev/null | grep 'Name:'", shell=True).decode().strip()
            window_manager = output.split(":")[1].strip()
            return window_manager
        except:
            pass
    return window_manager.capitalize() if window_manager else "Unknown"

def get_window_manager_theme():
    try:
        output = os.popen('gsettings get org.gnome.desktop.wm.preferences theme').read()
        return output.strip()
    except:
        return "Unknown"

def get_gtk_theme():
    try:
        output = os.popen('gsettings get org.gnome.desktop.interface gtk-theme').read()
        return output.strip()
    except:
        return "Unknown"

def get_icon_theme():
    try:
        output = os.popen('gsettings get org.gnome.desktop.interface icon-theme').read()
        return output.strip()
    except:
        return "Unknown"

def get_terminal():
    return os.environ.get('COLORTERM', "Unknown")

def print_color_strip():
    colors = [
        "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m",
        "\033[97m", "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"
    ]
    strip = "".join([color + "█" for color in colors])
    print(strip + "\033[0m")  # Reset color

def main():
    os_info = get_os_info()
    kernel = get_kernel_info()
    architecture = get_arch_info()
    cpu_name, cpu_cores = get_cpu_info()
    total_memory, used_memory = get_memory_info()
    uptime = get_uptime_info()
    hostname = get_hostname_info()
    user = get_user_info()
    gpu_info = get_gpu_info()
    package_manager_info = get_package_manager_info()
    resolution = get_resolution()
    desktop_environment = get_desktop_environment()
    window_manager = get_window_manager()
    window_manager_theme = get_window_manager_theme()
    gtk_theme = get_gtk_theme()
    icon_theme = get_icon_theme()
    terminal = get_terminal()
      
    print(f"User: {user}@{hostname}")
    print(f"OS: {os_info}")
    print(f"Kernel: {kernel}")
    print(f"Architecture: {architecture}")
    print(f"CPU: {cpu_name} ({cpu_cores} cores)")
    print(f"GPU: {gpu_info}")
    print(f"Memory: {used_memory / (1024 ** 3):.2f}GiB / {total_memory / (1024 ** 3):.2f}GiB")
    print(f"Uptime: {uptime}")
    print(f"Resolution: {resolution}")
    print(f"DE: {desktop_environment}")
    print(f"WM: {window_manager}")
    print(f"WM Theme: {window_manager_theme}")
    print(f"Theme: {gtk_theme}")
    print(f"Icons: {icon_theme}")
    print(f"Terminal: {terminal}")
    
    for manager, count in package_manager_info.items():
        print(f"{manager.capitalize()}: {count} packages")
    
    print_color_strip()

if __name__ == "__main__":
    main()
