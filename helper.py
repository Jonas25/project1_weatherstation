import os, time, socket

def sync_time():
    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('0.be.pool.ntp.org')
        os.system('sudo date ' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))
    except:
        print('Could not sync with time server.')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]
