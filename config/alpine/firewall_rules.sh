#!binsh

# 1. Bersihkan aturan lama
iptables -F FORWARD
iptables -F INPUT
iptables -t nat -F

# 2. Atur Policy Default (Blokir Forwarding)
iptables -P FORWARD DROP
iptables -P INPUT ACCEPT

# 3. Konfigurasi NAT (Agar bisa internetan)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# 4. Izinkan Koneksi Dasar
# Izinkan DHCP request masuk
iptables -I INPUT -p udp --dport 67 -j ACCEPT
# Izinkan paket balasan (ESTABLISHEDRELATED)
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 5. Akses Internet (Internal - Internet)
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth0 -j ACCEPT

# 6. Akses Internal ke Server
iptables -A FORWARD -i eth2 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth1 -j ACCEPT

# 7. Pengecualian Eksternal (Whitelist)
# Izinkan Ping ke Server
iptables -A FORWARD -i eth4 -o eth1 -d 192.168.10.024 -p icmp --icmp-type echo-request -j ACCEPT
# Izinkan SSH ke Server
iptables -A FORWARD -i eth4 -o eth1 -d 192.168.10.024 -p tcp --dport 22 -j ACCEPT
# Izinkan Aplikasi Data Sharing (Port 50001)
iptables -A FORWARD -i eth4 -o eth1 -d 192.168.10.024 -p tcp --dport 50001 -j ACCEPT

# 8. Konfigurasi VPN
# Izinkan koneksi VPN masuk (Port 1194)
iptables -A INPUT -p udp --dport 1194 -j ACCEPT
# Izinkan traffic dari VPN (tun0) ke Internal
iptables -A FORWARD -i tun0 -o eth1 -j ACCEPT
iptables -A FORWARD -i tun0 -o eth2 -j ACCEPT

# Simpan
rc-service iptables save
echo Firewall rules applied and saved.