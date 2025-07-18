import os
import pygame
import time
from pymavlink import mavutil
import config

def init_joystick():
    try:
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("[ERROR] Joystick not found! Please connect a joystick.")
            return None
        js = pygame.joystick.Joystick(0)
        js.init()
        print(f"[✓] Joystick connected: {js.get_name()}")
        return js
    except Exception as e:
        print(f"[ERROR] Joystick init failed: {e}")
        return None

def constrain(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def check_arm_status(master):
    hb = master.recv_match(type='HEARTBEAT', blocking=True)
    base_mode = hb.base_mode
    custom_mode = hb.custom_mode
    is_armed = (base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
    mode_str = master.mode_mapping().get(custom_mode, f"UNKNOWN({custom_mode})")
    return is_armed, mode_str

def run_manual(master):
    import __main__

    js = init_joystick()
    if js is None:
        print("[INFO] Manual control could not be started.")
        return

    is_armed, mode = check_arm_status(master)
    print(f"[INFO] Flight Mode: {mode}")
    print(f"[INFO] ARM Status: {'ARMED' if is_armed else 'DISARMED'}")

    print("[INFO] Sending initial neutral PWM signals...")
    master.mav.rc_channels_override_send(
        config.TARGET_SYSTEM,
        config.TARGET_COMPONENT,
        1500,  # RC1 → MAIN OUT 1
        1500,  # RC2 (unused)
        1500,  # RC3 → MAIN OUT 3
        1500, 1500, 1500, 1500, 1500
    )
    time.sleep(1)

    if not is_armed:
        print("[INFO] Arming vehicle...")
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
        master.motors_armed_wait()
        print("[✓] Vehicle armed.")

    print("[INFO] Manual PWM control started. Press Ctrl+C to stop.")
    try:
        while True:
            pygame.event.pump()

            thrust = -js.get_axis(1)  # Joystick Y ekseni (ileri/geri)
            steer = js.get_axis(0)   # Joystick X ekseni (sağ/sol)

            # PWM hesaplamaları (1000–2000 µs aralığı, merkez 1500)
            ch1_pwm = int(1500 + constrain(thrust + steer, -1, 1) * 400)
            ch3_pwm = int(1500 + constrain(thrust - steer, -1, 1) * 400)

            master.mav.rc_channels_override_send(
                config.TARGET_SYSTEM,
                config.TARGET_COMPONENT,
                ch1_pwm,
                1500,     # RC2
                ch3_pwm,
                1500, 1500, 1500, 1500, 1500
            )

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[INFO] Manual control stopped.")
        print("[INFO] Disarming vehicle...")

        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        master.motors_disarmed_wait()
        print("[✓] Vehicle disarmed.")

        print("[INFO] Returning to main menu...")
        os.execv(__main__.__file__, ['python3'] + [__main__.__file__])
