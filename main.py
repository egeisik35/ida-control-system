# -*- coding: utf-8 -*-
import subprocess
import sys

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
        print("1 - Launch MAVProxy Ground Station (Map, Telemetry, Mission Upload, Waypoint Selection)")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            launch_mavproxy()
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice! Please select 1 or 0.")

if __name__ == "__main__":
    main()
