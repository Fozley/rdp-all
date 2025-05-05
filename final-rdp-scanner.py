import threading
import socket

port = int(input("যে পোর্ট স্ক্যান করবেন (ডিফল্ট RDP 3389): ") or 3389)

max_threads = 1500
threads = []
output_file = "live_ips.txt"
scanned_file = "scannnn.txt"
lock = threading.Lock()

def check_rdp(ip):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"[+] Open: {ip}:{port}")
        with lock:
            with open(output_file, "a") as f:
                f.write(f"{ip}:{port}\n")
    except:
        pass
    finally:
        sock.close()
        # স্ক্যান করা আইপি সেভ করা
        with lock:
            with open(scanned_file, "a") as sf:
                sf.write(f"{ip}\n")

# ip_list.txt থেকে আইপি লোড করা
with open("ip_list.txt", "r") as f:
    ip_list = [line.strip() for line in f if line.strip()]

for ip in ip_list:
    while threading.active_count() > max_threads:
        pass
    t = threading.Thread(target=check_rdp, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"স্ক্যান শেষ। সক্রিয় আইপি {output_file} ফাইলে এবং স্ক্যান করা সব আইপি {scanned_file} ফাইলে সেভ করা হয়েছে।")