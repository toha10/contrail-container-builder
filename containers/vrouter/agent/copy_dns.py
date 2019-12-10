import dbus
import sys


DBUS_PROPS_IFACE = "org.freedesktop.DBus.Properties"
RESOLVED_BUS_NAME = "org.freedesktop.resolve1"
RESOLVED_LINK_IFACE = "org.freedesktop.resolve1.Link"
RESOLVED_MANAGER_IFACE = "org.freedesktop.resolve1.Manager"
RESOLVED_OBJ_PATH = "/org/freedesktop/resolve1"


def get_iface_obj_path(resolved_iface, iface_index):
    try:
        iface_obj_path = resolved_iface.GetLink(iface_index)
    except dbus.exceptions.DBusException:
        sys.exit("could not get link for {} interface "
                 "in resolved dbus".format(iface_index))

    return iface_obj_path


def main():

    if len(sys.argv) < 3:
        sys.exit("physical and virtual interface indexes "
                 "are required as first and second arguments")

    try:
        phys_iface_index, virt_iface_index = int(sys.argv[1]), int(sys.argv[2])
    except ValueError:
        sys.exit(
            "physical and virtual interface indexes should be integer numbers"
        )

    system_bus = dbus.SystemBus()

    resolve_iface = dbus.Interface(object=system_bus.get_object(
        RESOLVED_BUS_NAME, RESOLVED_OBJ_PATH),
        dbus_interface=RESOLVED_MANAGER_IFACE)

    phys_iface_proxy = system_bus.get_object(
        RESOLVED_BUS_NAME, get_iface_obj_path(resolve_iface, phys_iface_index))

    phys_iface_props_obj = dbus.Interface(phys_iface_proxy, DBUS_PROPS_IFACE)
    phys_iface_props = phys_iface_props_obj.GetAll(RESOLVED_LINK_IFACE)

    virt_iface_proxy = system_bus.get_object(
        RESOLVED_BUS_NAME, get_iface_obj_path(resolve_iface, virt_iface_index))
    vhost_iface_manager = dbus.Interface(virt_iface_proxy, RESOLVED_LINK_IFACE)

    vhost_iface_manager.SetDNS(phys_iface_props["DNS"])
    vhost_iface_manager.SetDomains(phys_iface_props["Domains"])


if __name__ == '__main__':
    main()
