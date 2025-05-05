import threading
import socket
import ipaddress

start_ip = input("Start IP দিন (যেমন: 192.168.0.1): ")
end_ip   = input("End IP দিন (যেমন: 192.168.0.254): ")
port     = 3389

max_threads = int(input("একসাথে কতটি থ্রেড চালাবেন (ডিফল্ট 500): ") or 500)

threads = []
output_file = "live_ips.txt"
lock = threading.Lock()

def check_rdp(ip):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((str(ip), port))
        print(f"[+] Open: {ip}:{port}")
        with lock:
            with open(output_file, "a") as f:
                f.write(f"{ip}:{port}\n")
    except:
        pass
    finally:
        sock.close()

for ip_int in range(int(ipaddress.IPv4Address(start_ip)), int(ipaddress.IPv4Address(end_ip)) + 1):
    ip = ipaddress.IPv4Address(ip_int)
    while threading.active_count() > max_threads:
        pass
    t = threading.Thread(target=check_rdp, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"স্ক্যান শেষ। সক্রিয় আইপি {output_file} ফাইলে সেভ করা হয়েছে।")
