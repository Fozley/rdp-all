import threading
import socket
import ipaddress
import sys
import time

start_ip = input("Start IP দিন (যেমন: 192.168.0.1): ")
end_ip   = input("End IP দিন (যেমন: 192.168.0.254): ")
port     = 3389

max_threads = int(input("একসাথে কতটি থ্রেড চালাবেন (ডিফল্ট 500): ") or 500)

threads = []
output_file = "live_ips.txt"
lock = threading.Lock()
current_ip = None  # কোন আইপি স্ক্যান হচ্ছে, এটা রাখবে

def check_rdp(ip):
    global current_ip
    try:
        current_ip = str(ip)
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

def wait_for_enter():
    while True:
        input()
        print(f"এখন স্ক্যান হচ্ছে: {current_ip}")

# ইনপুট থ্রেড চালু
input_thread = threading.Thread(target=wait_for_enter, daemon=True)
input_thread.start()

for ip_int in range(int(ipaddress.IPv4Address(start_ip)), int(ipaddress.IPv4Address(end_ip)) + 1):
    ip = ipaddress.IPv4Address(ip_int)
    while threading.active_count() > max_threads:
        time.sleep(0.01)
    t = threading.Thread(target=check_rdp, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"স্ক্যান শেষ। সক্রিয় আইপি {output_file} ফাইলে সেভ করা হয়েছে।")