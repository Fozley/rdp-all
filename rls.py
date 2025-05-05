import socket
import threading
import time

# ফাইল থেকে IP লোড
with open("ip_list.txt", "r") as file:
    ip_list = [line.strip() for line in file.readlines()]

lock = threading.Lock()

def scan(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        result = s.connect_ex((ip, 3389))

        with lock:
            with open("scaned_ip.txt", "a") as f:
                f.write(ip + "\n")

        if result == 0:
            with lock:
                with open("open_ips.txt", "a") as f:
                    f.write(ip + "\n")
                print(f"[+] Open: {ip}")

        s.close()
    except Exception:
        pass

threads = []
for ip in ip_list:
    while threading.active_count() > 800:
        time.sleep(0.01)
    t = threading.Thread(target=scan, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("স্ক্যান শেষ। সব আইপি scaned_ip.txt আর ওপেন আইপি open_ips.txt তে সেভ হয়েছে।"))