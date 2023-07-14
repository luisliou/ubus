from ubus import Ubus

ubus = Ubus(config_file='config.yaml')
# Login
has_logged_in = ubus.login()
if has_logged_in:
    # Perform ubus call, example calls network.interface status API
    return_data = ubus.call_ubus('network.interface.guest', 'status', {})
    if return_data is not None:
        print(return_data)

    # Logout
    ubus.logout()
