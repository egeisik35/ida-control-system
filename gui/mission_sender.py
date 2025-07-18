from pymavlink import mavutil
import config
import time

def send_mission(waypoints):
    print(f"[INFO] Connecting to vehicle on {config.CONNECTION_STRING}...")
    master = mavutil.mavlink_connection(config.CONNECTION_STRING, baud=config.BAUDRATE)
    master.wait_heartbeat()
    print(f"[✓] Connected. System ID: {master.target_system}, Component ID: {master.target_component}")

    print("[INFO] Clearing existing mission items...")
    master.mav.mission_clear_all_send(master.target_system, master.target_component)
    time.sleep(1)

    print(f"[INFO] Sending {len(waypoints)} mission items...")
    for i, (lat, lon, alt) in enumerate(waypoints):
        master.mav.mission_item_int_send(
            master.target_system,
            master.target_component,
            i,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 1,
            0, 0, 0, 0,
            int(lat * 1e7),
            int(lon * 1e7),
            float(alt)
        )
        time.sleep(0.1)

    master.mav.mission_count_send(master.target_system, master.target_component, len(waypoints))
    print("[✓] Mission uploaded.")

    while True:
        msg = master.recv_match(type=['MISSION_ACK', 'MISSION_REQUEST'], blocking=True)
        if msg.get_type() == 'MISSION_ACK':
            print(f"[✓] Mission acknowledged with result: {msg.type}")
            break
        elif msg.get_type() == 'MISSION_REQUEST':
            print(f"[INFO] Requested mission item: {msg.seq}")

def load_waypoints(filename="waypoints.txt"):
    waypoints = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                waypoints.append((float(parts[0]), float(parts[1]), float(parts[2])))
    return waypoints

if __name__ == "__main__":
    waypoints = load_waypoints()
    send_mission(waypoints)
