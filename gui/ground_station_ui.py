import tkinter as tk
import subprocess
import threading
from mission_sender import send_mission, load_waypoints
from control.auto_navigation import clear_mission, upload_mission, start_mission

def launch_kivy_selector():
    subprocess.run(["python3", "gui/waypoint_selector_kivy.py"])

def launch_gui(master):
    root = tk.Tk()
    root.title("Ground Station - Mission Control")

    tk.Button(root, text="Open Waypoint Selector", command=launch_kivy_selector).pack(pady=5)
    tk.Button(root, text="Send Mission", command=lambda: send_loaded_mission(master)).pack(pady=5)

    telemetry_frame = tk.Frame(root)
    telemetry_frame.pack(pady=10)
    label_lat = tk.Label(telemetry_frame, text="Lat: ---")
    label_lon = tk.Label(telemetry_frame, text="Lon: ---")
    label_heading = tk.Label(telemetry_frame, text="Heading: ---")
    label_speed = tk.Label(telemetry_frame, text="Speed: ---")
    label_pwm1 = tk.Label(telemetry_frame, text="PWM CH1: ---")
    label_pwm2 = tk.Label(telemetry_frame, text="PWM CH2: ---")
    label_lat.pack()
    label_lon.pack()
    label_heading.pack()
    label_speed.pack()
    label_pwm1.pack()
    label_pwm2.pack()

    def update_telemetry():
        try:
            msg = master.recv_match(type=["GLOBAL_POSITION_INT", "VFR_HUD", "RC_CHANNELS"], blocking=False)
            if msg:
                if msg.get_type() == "GLOBAL_POSITION_INT":
                    lat = msg.lat / 1e7
                    lon = msg.lon / 1e7
                    heading = msg.hdg / 100.0 if msg.hdg != 65535 else None
                    label_lat.config(text=f"Lat: {lat:.6f}")
                    label_lon.config(text=f"Lon: {lon:.6f}")
                    if heading is not None:
                        label_heading.config(text=f"Heading: {heading:.1f}°")
                elif msg.get_type() == "VFR_HUD":
                    label_speed.config(text=f"Speed: {msg.groundspeed:.2f} m/s")
                elif msg.get_type() == "RC_CHANNELS":
                    label_pwm1.config(text=f"PWM CH1: {msg.chan1_raw}")
                    label_pwm2.config(text=f"PWM CH2: {msg.chan2_raw}")
        except Exception as e:
            print(f"[ERROR] Telemetry update: {e}")
        root.after(500, update_telemetry)

    def send_loaded_mission(master):
        clear_mission(master)
        waypoints = load_waypoints()
        upload_mission(master, waypoints)
        start_mission(master)

    update_telemetry()
    root.mainloop()
