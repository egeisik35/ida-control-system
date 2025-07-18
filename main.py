# -*- coding: utf-8 -*-
import subprocess
import sys

# If these imports fail, make sure these modules/files exist in your repo!
try:
    import config
    from control.manual_control import run_manual
except ImportError:
    print("[ERROR] Could not import control modules. Manual control will not be available.")

def launch_mavproxy():
    """
    Launch MAVProxy with map and console modules for ground station functionality.
    """
    # Adjust connection string for your setup (e.g., serial, udp, etc.)
    connection = "udp:127.0.0.1:14550"
    cmd = [
        "mavproxy.py",
        f"--master={connection}",
        "--console",
        "--map"
    ]
    print(f"[INFO] Launching MAVProxy with: {' '.join(cmd)}")
    subprocess.run(cmd)

def main():
    while True:
        print("\n=== IDA CONTROL SYSTEM ===")
        print("1 - Manual Control (Joystick)")
        print("2 - Launch MAVProxy Ground Station (Map, Telemetry, Mission Upload, Waypoint Selection)")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Manual control (joystick) via your Python code
            try:
                from pymavlink import mavutil
                # Use connection settings from config.py if available
                conn_str = getattr(config, "MAVLINK_CONNECTION_STRING", "udp:127.0.0.1:14550")
                baud = getattr(config, "MAVLINK_BAUDRATE", 115200)
                print(f"[INFO] Connecting to vehicle on {conn_str} (baud {baud})...")
                master = mavutil.mavlink_connection(conn_str, baud=baud)
                master.wait_heartbeat()
                print(f"[✓] Connected to system {master.target_system}, component {master.target_component}")
                run_manual(master)
            except Exception as e:
                print(f"[ERROR] Manual control failed: {e}")
        elif choice == "2":
            # Launch MAVProxy for full ground station functionality
            launch_mavproxy()
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice! Please select 1, 2, or 0.")

if __name__ == "__main__":
    main()
