import os
import platform
import psutil
import socket
import subprocess
from datetime import datetime
import distro
import cpuinfo
import GPUtil
import argparse

def get_os_info():
    if platform.system() == "Linux":
        dist_name = distro.name(pretty=True)
        return dist_name
    else:
        return f"{platform.system()} {platform.release()}"

def get_kernel_info():
    return platform.release()

def get_battery_info():
    if psutil.sensors_battery():
        battery = psutil.sensors_battery()
        percent = battery.percent
        status = "Charging" if battery.power_plugged else "Discharging"
        return f"{percent}% [{status}]"
    return "No Battery"

def get_disk_usage_info():
    disk_partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in disk_partitions:
        if partition.mountpoint.startswith("/snap"):
            continue
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.mountpoint] = (usage.total, usage.used)
    return disk_usage

def get_swap_info():
    swap = psutil.swap_memory()
    return swap.total, swap.used

def get_arch_info():
    return platform.machine()

def get_cpu_info():
    cpu = cpuinfo.get_cpu_info()
    cpu_name = cpu['brand_raw']
    cpu_cores = psutil.cpu_count(logical=True)
    return cpu_name, cpu_cores

def get_local_ip_info(interface='wlo1'):
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        if ip_address.startswith("127."):
            interfaces = psutil.net_if_addrs()
            for iface in interfaces.get(interface, []):
                if iface.family == socket.AF_INET:
                    return iface.address
    except Exception as e:
        pass
    return "Unknown"

def get_memory_info():
    mem = psutil.virtual_memory()
    return mem.total, mem.used

def get_locale_info():
    return os.environ.get('LANG', 'Unknown')

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
        output = subprocess.check_output('xrandr | grep "*" | awk \'{print $1}\'', shell=True).decode().strip()
        if output:
            return output
        else:
            output = subprocess.check_output('xdpyinfo | grep dimensions', shell=True).decode().strip()
            resolution = output.split()[1]
            return resolution
    except:
        return "Unknown"

def get_desktop_environment():
    desktop_session = os.environ.get('DESKTOP_SESSION', "").lower()
    if "zorin" in desktop_session:
        return "Zorin"
    elif "gnome" in desktop_session:
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
    try:
        output = subprocess.check_output("echo $XDG_SESSION_TYPE", shell=True).decode().strip().lower()
        if output == "wayland":
            return "Wayland"
        elif output == "x11":
            try:
                wm_output = subprocess.check_output("wmctrl -m | grep 'Name:'", shell=True).decode().strip()
                window_manager = wm_output.split(":")[1].strip()
                return window_manager
            except:
                pass
    except:
        pass
    return "Unknown"

def get_window_manager_theme():
    try:
        # For GNOME
        if "gnome" in os.environ.get('DESKTOP_SESSION', "").lower():
            output = subprocess.check_output('gsettings get org.gnome.desktop.wm.preferences theme', shell=True).decode().strip()
            return output.strip("'")

        # For KDE Plasma
        if "kde" in os.environ.get('DESKTOP_SESSION', "").lower():
            output = subprocess.check_output('kreadconfig5 --group WM --key theme', shell=True).decode().strip()
            return output

        # For Zorin
        if "zorin" in os.environ.get('DESKTOP_SESSION', "").lower():
            output = subprocess.check_output('gsettings get org.gnome.desktop.wm.preferences theme', shell=True).decode().strip()
            return output.strip("'")
    except:
        pass
    return "Unknown"

def get_gtk_theme():
    try:
        output = subprocess.check_output('gsettings get org.gnome.desktop.interface gtk-theme', shell=True).decode().strip()
        return output.strip("'")
    except:
        return "Unknown"

def get_icon_theme():
    try:
        output = subprocess.check_output('gsettings get org.gnome.desktop.interface icon-theme', shell=True).decode().strip()
        return output.strip("'")
    except:
        return "Unknown"

def get_terminal():
    term = os.environ.get('TERM', "Unknown")
    colorterm = os.environ.get('COLORTERM', "")
    terminal = os.environ.get('TERMINAL', "")
    
    if terminal:
        return terminal
    elif colorterm:
        return colorterm
    else:
        return term

def get_terminal_font():
    try:
        # For GNOME Terminal
        output = subprocess.check_output('gsettings get org.gnome.desktop.interface monospace-font-name', shell=True).decode().strip()
        if output:
            return output.strip("'")
    except:
        pass

    try:
        # For KDE Konsole
        output = subprocess.check_output('konsole --list-profiles', shell=True).decode().strip().split("\n")
        profile = output[0]
        output = subprocess.check_output(f'konsoleprofile "Profile: {profile}" -p font', shell=True).decode().strip()
        if output:
            return output
    except:
        pass

    return "Unknown"

def get_system_font():
    try:
        # For GNOME
        if "gnome" in os.environ.get('DESKTOP_SESSION', "").lower():
            output = subprocess.check_output('gsettings get org.gnome.desktop.interface font-name', shell=True).decode().strip()
            return output.strip("'")

        # For KDE
        if "kde" in os.environ.get('DESKTOP_SESSION', "").lower():
            output = subprocess.check_output('kreadconfig5 --group General --key font', shell=True).decode().strip()
            return output
    except:
        pass

    return "Unknown"

def print_color_strip():
    colors = [
        "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m",
        "\033[97m", "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"
    ]
    strip = "".join([color + "█" for color in colors])
    print(strip + "\033[0m")  # Reset color

def get_distro_logo(distro_name):
    logos = {
        "Zorin OS": """
\033[36m        ██████████        \033[0m
\033[36m    ████████████████    \033[0m
\033[36m  ████████████████████  \033[0m
\033[36m████████████████████████\033[0m
\033[36m████████████████████████\033[0m
\033[36m████████████████████████\033[0m
\033[36m████████████████████████\033[0m
\033[36m  ████████████████████  \033[0m
\033[36m    ████████████████    \033[0m
\033[36m        ██████████        \033[0m
""",
        # Add more ASCII logos for other supported distros here
    }
    return logos.get(distro_name, "Unsupported distro for artwork display")

def main():
    parser = argparse.ArgumentParser(description="QuickFetch System Information")
    parser.add_argument("--experimental", action="store_true", help="Display with artwork similar to Neofetch")
    args = parser.parse_args()

    os_info = get_os_info()
    kernel = get_kernel_info()
    architecture = get_arch_info()
    cpu_name, cpu_cores = get_cpu_info()
    total_memory, used_memory = get_memory_info()
    swap_total, swap_used = get_swap_info()
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
    terminal_font = get_terminal_font()
    system_font = get_system_font()
    disk_usage_info = get_disk_usage_info()
    local_ip = get_local_ip_info()
    battery_info = get_battery_info()
    locale_info = get_locale_info()

    if args.experimental:
        logo = get_distro_logo(os_info)
        if logo == "Unsupported distro for artwork display":
            print(f"User: {user}@{hostname}")
            print(f"OS: {os_info}")
            print(f"Kernel: {kernel}")
            print(f"Architecture: {architecture}")
            print(f"CPU: {cpu_name} ({cpu_cores} cores)")
            print(f"GPU: {gpu_info}")
            print(f"Memory: {used_memory / (1024 ** 3):.2f}GiB / {total_memory / (1024 ** 3):.2f}GiB")
            print(f"Swap: {swap_used / (1024 ** 3):.2f}GiB / {swap_total / (1024 ** 3):.2f}GiB")
            print(f"Uptime: {uptime}")
            print(f"Resolution: {resolution}")
            print(f"DE: {desktop_environment}")
            print(f"WM: {window_manager}")
            print(f"WM Theme: {window_manager_theme}")
            print(f"Theme: {gtk_theme}")
            print(f"Icons: {icon_theme}")
            print(f"Terminal: {terminal}")
            print(f"Terminal Font: {terminal_font}")
            print(f"System Font: {system_font}")
            for mountpoint, (total, used) in disk_usage_info.items():
                print(f"Disk ({mountpoint}): {used / (1024 ** 3):.2f}GiB / {total / (1024 ** 3):.2f}GiB")
            print(f"Local IP: {local_ip}")
            print(f"Battery: {battery_info}")
            print(f"Locale: {locale_info}")
            for manager, count in package_manager_info.items():
                print(f"{manager.capitalize()}: {count} packages")
            print_color_strip()
        else:
            print(logo)
            details = f"""
User: {user}@{hostname}
OS: {os_info}
Kernel: {kernel}
Architecture: {architecture}
CPU: {cpu_name} ({cpu_cores} cores)
GPU: {gpu_info}
Memory: {used_memory / (1024 ** 3):.2f}GiB / {total_memory / (1024 ** 3):.2f}GiB
Swap: {swap_used / (1024 ** 3):.2f}GiB / {swap_total / (1024 ** 3):.2f}GiB
Uptime: {uptime}
Resolution: {resolution}
DE: {desktop_environment}
WM: {window_manager}
WM Theme: {window_manager_theme}
Theme: {gtk_theme}
Icons: {icon_theme}
Terminal: {terminal}
Terminal Font: {terminal_font}
System Font: {system_font}
Local IP: {local_ip}
Battery: {battery_info}
Locale: {locale_info}"""
            for mountpoint, (total, used) in disk_usage_info.items():
                details += f"\nDisk ({mountpoint}): {used / (1024 ** 3):.2f}GiB / {total / (1024 ** 3):.2f}GiB"
            for manager, count in package_manager_info.items():
                details += f"\n{manager.capitalize()}: {count} packages"
            print(details)
            print_color_strip()
    else:
        print(f"User: {user}@{hostname}")
        print(f"OS: {os_info}")
        print(f"Kernel: {kernel}")
        print(f"Architecture: {architecture}")
        print(f"CPU: {cpu_name} ({cpu_cores} cores)")
        print(f"GPU: {gpu_info}")
        print(f"Memory: {used_memory / (1024 ** 3):.2f}GiB / {total_memory / (1024 ** 3):.2f}GiB")
        print(f"Swap: {swap_used / (1024 ** 3):.2f}GiB / {swap_total / (1024 ** 3):.2f}GiB")
        print(f"Uptime: {uptime}")
        print(f"Resolution: {resolution}")
        print(f"DE: {desktop_environment}")
        print(f"WM: {window_manager}")
        print(f"WM Theme: {window_manager_theme}")
        print(f"Theme: {gtk_theme}")
        print(f"Icons: {icon_theme}")
        print(f"Terminal: {terminal}")
        print(f"Terminal Font: {terminal_font}")
        print(f"System Font: {system_font}")
        for mountpoint, (total, used) in disk_usage_info.items():
            print(f"Disk ({mountpoint}): {used / (1024 ** 3):.2f}GiB / {total / (1024 ** 3):.2f}GiB")
        print(f"Local IP: {local_ip}")
        print(f"Battery: {battery_info}")
        print(f"Locale: {locale_info}")
        for manager, count in package_manager_info.items():
            print(f"{manager.capitalize()}: {count} packages")
        print_color_strip()

if __name__ == "__main__":
    main()
