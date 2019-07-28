import network
import time
import sys
# import webrepl

def do_connect(verbose = True):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    creddict = {}
    ssid_pass = None
    for credline in open('cred.txt').readlines():
        try:
            credline=credline.strip()
            if credline.startswith('#'):
                continue
            if credline.startswith('hostname'):
                # This shows up in your router.
                wlan.config(dhcp_hostname=credline.split(':')[1].strip())
            role, name, password = [s.strip() for s in credline.split(":")]
            if role.lower() == 'wificlient':
                creddict[name] = password
            elif role.lower() == 'wifihost':
                ssid_pass = name, password
        except:
            pass
    netnames = []
    for nets in wlan.scan():
        try:
            netname = nets[0].decode()
            netnames.append(netname)
            try:
                wlan.connect(netname, creddict[netname])
                if verbose:
                    print('Connecting to network', netname, file=sys.stderr)
                while wlan.status() is network.STAT_CONNECTING:
                    time.sleep(0.1)
                for i in range(10):
                    if wlan.isconnected():
                        try:
                            ssid_pass = ssid_pass[0]+wlan.ifconfig()[0], ssid_pass[1]
                        except:
                            pass
                        if verbose:
                            if verbose:
                                print("Connected to network {} and IP = {}"
                                             .format(netname,
                                                     wlan.ifconfig()[0]),
                                file = sys.stderr)
                        break
                    time.sleep(1)
                else:
                    continue
                break   # Connected
            except Exception as e:
                if verbose:
                    print("Exception ", e, file=sys.stderr)
                pass
        except KeyError:
            pass
    else:
        if verbose:
            print("Could not connect to any networks among", netnames, file=sys.stderr)
    if ssid_pass:
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid_pass[0])
        if ssid_pass[1]:
            ap.config(password=ssid_pass[1])
        if verbose:
            print("AP set up as {}".format(ssid_pass[0]), file=sys.stderr)

