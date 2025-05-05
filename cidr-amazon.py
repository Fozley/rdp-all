import ipaddress

# ইউজার থেকে CIDR ফাইলের নাম ইনপুট নেওয়া
filename = input("CIDR লিস্ট ফাইলের নাম লিখুন (উদা: cidr_list.txt): ")

try:
    with open(filename, 'r') as f:
        cidr_list = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"{filename} ফাইল পাওয়া যায়নি।")
    exit()

def generate_ips(cidr_ranges, batch_size=200000):
    count = 0
    output_file = "generated_ips.txt"

    with open(output_file, "w") as f:
        for cidr in cidr_ranges:
            try:
                network = ipaddress.ip_network(cidr)
                for ip in network.hosts():
                    f.write(str(ip) + "\n")
                    count += 1
                    if count % batch_size == 0:
                        print(f"{count} টি IP তৈরি হয়েছে। চালিয়ে যেতে Enter চাপুন...")
                        input()
            except ValueError as e:
                print(f"{cidr} সঠিক CIDR নয়: {e}")
    
    print(f"মোট {count} টি IP তৈরি হয়েছে। ফলাফল: {output_file}")

# কাজ শুরু
generate_ips(cidr_list)