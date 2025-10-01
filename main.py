from Scripts.wide_angle_camera import access_wide_angle_camera
from Scripts.stand_sit import send_stand_sit_command
from Scripts.stop_robot import send_stop_command
from Scripts.reset_to_zero import send_reset_to_zero_command
from Scripts.heartbeat import start_heartbeat

def main():
    hb_thread, hb_stop = start_heartbeat()

    try:
        while True:
            print("\nRobot Control Menu:")
            print("1. Wide-Angle Camera")
            print("2. Stand/Sit")
            print("3. STOP")
            print("4. Reset to Zero")
            print("5. Access Subcategories")
            print("6. Exit")
            print("\nDeveloped by: Ibrahim :)")

            choice = input("Select an option (1-6): ").strip() 

            if choice == "1":
                access_wide_angle_camera()
            elif choice == "2":
                send_stand_sit_command()
            elif choice == "3":
                send_stop_command()
            elif choice == "4":
                send_reset_to_zero_command()
            elif choice == "5":
                access_subcategories()
            elif choice == "6":
                print("Exiting the Robot Control Program. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        # Stop heartbeat cleanly
        hb_stop.set()
        hb_thread.join(timeout=1)

def access_subcategories():
    while True:
        print("\nSubcategories:")
        print("1. Misc")
        print("2. Standing Modes")
        print("3. Robot Movement")
        print("4. Actions")
        print("5. Gears")
        print("6. Functions")
        print("7. Back to Main Menu")

        category_choice = input("Select a category (1-7): ").strip()

        if category_choice == "1":
            access_misc()
        elif category_choice == "2":
            access_standing_modes()
        elif category_choice == "3":
            access_robot_movement()
        elif category_choice == "4":
            access_actions()
        elif category_choice == "5":
            access_gears()
        elif category_choice == "6":
            access_functions()
        elif category_choice == "7":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_misc():
    from Scripts.Misc.head_down import move_head_down
    from Scripts.Misc.head_up import move_head_up
    from Scripts.Misc.turn_left_90 import turn_left_90
    from Scripts.Misc.turn_right_90 import turn_right_90
    from Scripts.Misc.turn_back_180 import turn_back_180
    from Scripts.Misc.stop_movement import stop_movement

    while True:
        print("\nMisc Commands:")
        print("1. Move Head Down")
        print("2. Move Head Up")
        print("3. Turn Left by 90°")
        print("4. Turn Right by 90°")
        print("5. Turn Back by 180°")
        print("6. Stop Movement")
        print("7. Back to Subcategories")

        misc_choice = input("Select an option (1-7): ").strip()

        if misc_choice == "1":
            move_head_down()
        elif misc_choice == "2":
            move_head_up()
        elif misc_choice == "3":
            turn_left_90()
        elif misc_choice == "4":
            turn_right_90()
        elif misc_choice == "5":
            turn_back_180()
        elif misc_choice == "6":
            stop_movement()
        elif misc_choice == "7":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_standing_modes():
    from Scripts.Standing_Modes.pose_mode import switch_to_pose_mode
    from Scripts.Standing_Modes.move_mode import switch_to_move_mode

    while True:
        print("\nStanding Modes:")
        print("1. Switch to Pose Mode")
        print("2. Switch to Move Mode")
        print("3. Back to Subcategories")

        standing_choice = input("Select an option (1-3): ").strip()

        if standing_choice == "1":
            switch_to_pose_mode()
        elif standing_choice == "2":
            switch_to_move_mode()
        elif standing_choice == "3":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_robot_movement():
    from Scripts.Robot_Movement.navigation_mode import switch_to_navigation_mode
    from Scripts.Robot_Movement.manual_mode import switch_to_manual_mode
    from Scripts.Robot_Movement.angular_velocity import set_angular_velocity
    from Scripts.Robot_Movement.linear_velocity_x import set_linear_velocity_x
    from Scripts.Robot_Movement.linear_velocity_y import set_linear_velocity_y
    from Scripts.Robot_Movement.combined_velocity import set_combined_velocity
    from Scripts.Robot_Movement.enable_keep_stepping import enable_keep_stepping_mode
    from Scripts.Robot_Movement.disable_keep_stepping import disable_keep_stepping_mode

    while True:
        print("\nRobot Movement:")
        print("1. Switch to Navigation Mode")
        print("2. Switch to Manual Mode")
        print("3. Set Angular Velocity")
        print("4. Set Linear Velocity (X-axis)")
        print("5. Set Linear Velocity (Y-axis)")
        print("6. Set Combined Velocity")
        print("7. Enable Keep Stepping Mode")
        print("8. Disable Keep Stepping Mode")
        print("9. Back to Subcategories")

        movement_choice = input("Select an option (1-9): ").strip()

        if movement_choice == "1":
            switch_to_navigation_mode()
        elif movement_choice == "2":
            switch_to_manual_mode()
        elif movement_choice == "3":
            set_angular_velocity()
        elif movement_choice == "4":
            set_linear_velocity_x()
        elif movement_choice == "5":
            set_linear_velocity_y()
        elif movement_choice == "6":
            set_combined_velocity()
        elif movement_choice == "7":
            enable_keep_stepping_mode()
        elif movement_choice == "8":
            disable_keep_stepping_mode()
        elif movement_choice == "9":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_actions():
    from Scripts.Actions.twist import perform_twist
    from Scripts.Actions.turn_over import perform_turn_over
    from Scripts.Actions.moonwalk import perform_moonwalk
    from Scripts.Actions.backflip import perform_backflip
    from Scripts.Actions.hello import perform_hello
    from Scripts.Actions.long_jump import perform_long_jump
    from Scripts.Actions.twist_jump import perform_twist_jump

    while True:
        print("\nActions:")
        print("1. Perform Twist")
        print("2. Perform Turn Over")
        print("3. Perform Moonwalk")
        print("4. Perform Backflip")
        print("5. Perform Hello")
        print("6. Perform Long Jump")
        print("7. Perform Twist Jump")
        print("8. Back to Subcategories")

        action_choice = input("Select an option (1-8): ").strip()

        if action_choice == "1":
            perform_twist()
        elif action_choice == "2":
            perform_turn_over()
        elif action_choice == "3":
            perform_moonwalk()
        elif action_choice == "4":
            perform_backflip()
        elif action_choice == "5":
            perform_hello()
        elif action_choice == "6":
            perform_long_jump()
        elif action_choice == "7":
            perform_twist_jump()
        elif action_choice == "8":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_gears():
    from Scripts.Gears.slow_gear import switch_to_slow_gear
    from Scripts.Gears.medium_gear import switch_to_medium_gear
    from Scripts.Gears.fast_gear import switch_to_fast_gear
    from Scripts.Gears.crawl_gear import switch_to_crawl_gear
    from Scripts.Gears.grip_gear import switch_to_grip_gear
    from Scripts.Gears.general_gear import switch_to_general_gear
    from Scripts.Gears.h_step_gear import switch_to_h_step_gear

    while True:
        print("\nGears:")
        print("1. Switch to Flat gait in Slow gear")
        print("2. Switch to Flat gait in Medium gear")
        print("3. Switch to Flat gait in Fast gear")
        print("4. Switch to Flat gait in Crawl gear")
        print("5. Switch to RUG gait in Grip gear")
        print("6. Switch to RUG gait in General gear")
        print("7. Switch to RUG gait in H-Step gear")
        print("8. Back to Subcategories")

        gear_choice = input("Select an option (1-8): ").strip()

        if gear_choice == "1":
            switch_to_slow_gear()
        elif gear_choice == "2":
            switch_to_medium_gear()
        elif gear_choice == "3":
            switch_to_fast_gear()
        elif gear_choice == "4":
            switch_to_crawl_gear()
        elif gear_choice == "5":
            switch_to_grip_gear()
        elif gear_choice == "6":
            switch_to_general_gear()
        elif gear_choice == "7":
            switch_to_h_step_gear()
        elif gear_choice == "8":
            break
        else:
            print("Invalid choice. Please select a valid option.")

def access_functions():
    from Scripts.Functions.turn_off_ai import turn_off_ai
    from Scripts.Functions.enable_auto_stop import enable_auto_stop
    from Scripts.Functions.enable_tracking import enable_tracking
    from Scripts.Functions.enable_obstacle_avoidance import enable_obstacle_avoidance

    while True:
        print("\nFunctions:")
        print("1. Turn Off All AI Options")
        print("2. Enable Auto Stop Function")
        print("3. Enable Tracking Function")
        print("4. Enable Obstacle Avoidance Function")
        print("5. Back to Subcategories")

        function_choice = input("Select an option (1-5): ").strip()

        if function_choice == "1":
            turn_off_ai()
        elif function_choice == "2":
            enable_auto_stop()
        elif function_choice == "3":
            enable_tracking()
        elif function_choice == "4":
            enable_obstacle_avoidance()
        elif function_choice == "5":
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
