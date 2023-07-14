from ubus import Ubus
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'ubus_config.yaml'
    ubus = Ubus(config_file=config_file)
    # Login
    has_logged_in = ubus.login()
    if has_logged_in:
        return_data = ubus.call_ubus('network.interface.guest', 'status', {})
        if return_data is not None:
            print(return_data)

        # Logout
        ubus.logout()
