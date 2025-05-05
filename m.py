import ipaddress

input_file = "ranges.txt"
output_file = "generated_ips.txt"

batch_size = 2000000  # প্রতি কত আইপি পরে থামবে
ip_count = 0

# রেঞ্জ লোড করে উল্টো করা
with open(input_file, "r") as f:
    ranges = f.readlines()[::-1]  # উল্টো করে নিলাম

with open(output_file, "w") as out_f:
    for line in ranges:
        start_ip, end_ip = line.strip().split(",")
        start_int = int(ipaddress.IPv4Address(start_ip))
        end_int = int(ipaddress.IPv4Address(end_ip))

        for ip_int in range(start_int, end_int + 1):
            ip = str(ipaddress.IPv4Address(ip_int))
            out_f.write(ip + "\n")
            ip_count += 1

            if ip_count % batch_size == 0:
                print(f"{ip_count} টি আইপি জেনারেট হয়েছে। চালিয়ে যেতে Enter চাপুন...")
                input()  # ইউজারের Enter চাপা পর্যন্ত অপেক্ষা করবে

print(f"সব আইপি {output_file} ফাইলে সেভ করা হয়েছে। মোট {ip_count} আইপি।")