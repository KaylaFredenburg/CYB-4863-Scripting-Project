import os
import subprocess
import platform
import json
from datetime import datetime

# Import winreg only on Windows
if platform.system() == "Windows":
    import winreg

# Get list of active users
def get_users():
    output = subprocess.check_output(['net', 'users']).decode('utf-8')
    users = [line.strip() for line in output.split('\n') if line.strip() and not line.startswith('The command completed successfully.')]
    return {"active_users": users}

# Get list of installed software (Windows only)
def get_installed_software():
    # Check if running on Windows
    if platform.system() != "Windows":
        return ["Not supported on this OS"]
    
    # Initialize software list
    software_list = []
    # Define registry paths to check
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    # Loop through registry paths
    for reg_path in registry_paths:
        try:
            # Open registry key
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg:
                # Loop through subkeys
                for i in range(0, winreg.QueryInfoKey(reg)[0]):
                    try:
                        # Get subkey name
                        subkey_name = winreg.EnumKey(reg, i)
                        # Open subkey
                        with winreg.OpenKey(reg, subkey_name) as subkey:
                            # Get software name and version
                            name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                            version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                            # Add to software list
                            software_list.append({"name": name, "version": version})
                    except EnvironmentError:
                        # Skip if error occurs
                        continue
        except Exception as e:
            # Add error to software list
            software_list.append({"error": str(e)})
    return software_list

# Get list of missing security patches
def get_missing_security_patches():
    # Initialize patches list
    patches = []
    try:
        # Run command to get list of security patches
        output = subprocess.check_output("wmic qfe get HotFixID, InstalledOn", shell=True).decode()
        # Parse output
        patches = [line.strip() for line in output.split("\n") if line.strip()]
    except Exception as e:
        # Add error to patches list
        patches.append(f"Error: {str(e)}")
    return patches

# Get list of previously connected USB devices (Windows only)
def get_usb_history():
    # Check if running on Windows
    if platform.system() != "Windows":
        return ["Not supported on this OS"]
    
    # Initialize USB device list
    usb_list = []
    # Define registry path to check
    reg_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
    
    try:
        # Open registry key
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg:
            # Loop through subkeys
            for i in range(0, winreg.QueryInfoKey(reg)[0]):
                try:
                    # Get subkey name
                    subkey_name = winreg.EnumKey(reg, i)
                    print(subkey_name)
                    # Open subkey
                    with winreg.OpenKey(reg, subkey_name) as subkey:
                        # Loop through sub-subkeys
                        for j in range(0, winreg.QueryInfoKey(subkey)[0]):
                            try:
                                # Get sub-subkey name
                                subsubkey_name = winreg.EnumKey(subkey, j)
                                print(subsubkey_name)
                                # Open sub-subkey
                                with winreg.OpenKey(subkey, subsubkey_name) as subsubkey:
                                    # Get USB device name
                                    name, _ = winreg.QueryValueEx(subsubkey, "FriendlyName")
                                    print(name)
                                    # Add to USB list
                                    usb_list.append({"name": name})
                            except EnvironmentError:
                                # Skip if error occurs
                                continue
                except EnvironmentError:
                    # Skip if error occurs
                    continue
    except Exception as e:
        # Add error to software list
        usb_list.append({"error": str(e)})
    return usb_list
    
# Main function
def main():
    # Get desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "system_inventory.json")
    
    # Initialize system info dictionary
    system_info = {
        "timestamp": str(datetime.now()),
        "os": platform.system() + " " + platform.version(),
        "active_users": get_active_users(),
        "installed_software": get_installed_software(),
        "missing_security_patches": get_missing_security_patches(),
        "usb_history": get_usb_history()
    }
    
    # Save system info to JSON file
    with open(desktop_path, "w") as f:
        json.dump(system_info, f, indent=4)
    
    # Print success message
    print(f"System inventory recorded at: {desktop_path}")

# Run main function
if __name__ == "__main__":
    main()
