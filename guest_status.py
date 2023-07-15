from ubus import Ubus
import sys

if __name__ == "__main__":
    config_file = 'ubus_config.yaml'
    is_change_status = False
    enable = False
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        if len(sys.argv) > 2:
            is_change_status = True
            enable = sys.argv[2]
    ubus = Ubus(config_file=config_file)
    # Login
    has_logged_in = ubus.login()
    if has_logged_in:
        if is_change_status:
            if enable == 'true':
                guest_command = 'up'
            else:
                guest_command = 'down'
            return_data = ubus.call_ubus('network.interface.guest', guest_command, {})
        else:
            return_data = ubus.call_ubus('network.interface.guest', 'status', {})
        if return_data is not None:
            print(return_data)

        # Logout
        ubus.logout()
