import network
import time
import sys
# import webrepl

def do_connect(verbose = True):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    creddict = {}
    hostpass = None
    for credline in open('cred.txt').readlines():
        try:
            if credline.strip().startswith('#'):
                continue
            role, name, password = [s.strip() for s in credline.split(":")]
            if role.lower() == 'wificlient':
                creddict[name] = password
            elif role.lower() == 'wifihost':
                hostpass = name, password
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
    if hostpass:
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=hostpass[0])
        if hostpass[1]:
            ap.config(password=hostpass[1])
        if verbose:
            print("AP set up as {}".format(hostpass[0]), file=sys.stderr)

