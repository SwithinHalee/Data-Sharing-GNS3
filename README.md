# Secure Data Exchange System (SDES) 🛡️

[![Project Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Alpine_Linux-lightgrey.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Secure Data Exchange System (SDES)** adalah simulasi lengkap infrastruktur IT yang aman. Proyek ini menggabungkan pemrograman aplikasi (Python) dengan rekayasa jaringan (Network Engineering) menggunakan GNS3.

Sistem ini mensimulasikan lingkungan perusahaan dimana jaringan internal dilindungi oleh Firewall ketat, dan akses dari luar hanya dimungkinkan melalui jalur VPN yang terenkripsi.

---

## 📑 Daftar Isi
1.  [Persiapan & Download](#1-persiapan--download-bahan)
2.  [Arsitektur Jaringan](#2-arsitektur-jaringan)
3.  [Instalasi Infrastruktur (GNS3)](#3-instalasi-infrastruktur-gns3)
4.  [Konfigurasi Router (Alpine Linux)](#4-konfigurasi-router-alpine-linux)
5.  [Setup Aplikasi Python](#5-setup-aplikasi-python)
6.  [Setup VPN (Akses Eksternal)](#6-setup-vpn-akses-eksternal)
7.  [Cara Penggunaan & Demo](#7-cara-penggunaan--demo)

---

## 1. Persiapan & Download Bahan

Sebelum memulai, pastikan Anda memiliki semua *software* dan *firmware* berikut.

### A. Software Utama (Wajib Install di Laptop)
| Software | Kegunaan | Link Download |
| :--- | :--- | :--- |
| **GNS3** | Simulator Jaringan Utama | [Download GNS3](https://www.gns3.com/software/download) (Wajib Login) |
| **GNS3 VM** | Mesin virtual agar GNS3 stabil | [Download GNS3 VM](https://github.com/GNS3/gns3-gui/releases) (Pilih yg sesuai VirtualBox) |
| **VirtualBox** | Menjalankan OS Virtual | [Download VirtualBox](https://www.virtualbox.org/wiki/Downloads) |

### B. Image Sistem Operasi (ISO)
Unduh file ISO ini untuk dimasukkan ke dalam VirtualBox/GNS3 sebagai host:
| OS Name | Peran | Versi Disarankan | Link Download |
| :--- | :--- | :--- | :--- |
| **Alpine Linux** | Router & Firewall (Ringan) | Standard (x86_64) | [Download ISO](https://alpinelinux.org/downloads/) |
| **Ubuntu Server** | Server Aplikasi Data | 24.04 LTS | [Download ISO](https://ubuntu.com/download/server) |
| **Lubuntu** | Klien (User Interface Ringan) | LTS Version | [Download ISO](https://lubuntu.me/downloads/) |

### C. Cisco IOS Images (Penyedia Infrastruktur)
File-file berikut **telah disediakan di dalam repository ini** (folder `firmware`). Silakan download dan import ke GNS3 untuk menjalankan simulasi Router dan Switch Cisco.

| Filename | Tipe Perangkat | Kegunaan di GNS3 | Link Download |
| :--- | :--- | :--- | :--- |
| `c3745-advipservicesk9-mz.124-25d.bin` | **Router c3745** | Router Cisco (Opsional/Cadangan) | [📥 Download File](https://drive.google.com/file/d/1O6AnGK3xX9f8ity1pocyPBdTfAavtSiJ/view?usp=drive_link) |
| `c7200-adventerprisek9-mz.124-24.T5.bin` | **Router c7200** | Router Utama (High-Performance) | [📥 Download File](https://drive.google.com/file/d/1fY50E_TfKkxZmei0AY_cksDGuJ6wXhLq/view?usp=drive_link) |
| `i86bi-linux-l2-ipbasek9-15.1g.bin` | **Switch L2 (IOU)** | Ethernet Switch Antar-Zona | [📥 Download File](https://drive.google.com/file/d/1sRTdCfTsfuI0adbJerZmIppKB5Uq4Fas/view?usp=drive_link) |
| `cisco-asav-9.x.x.zip` | **Cisco ASAv** | Next-Gen Firewall & VPN (Enterprise) | [📥 Download File](https://drive.google.com/file/d/1-1K3ukjRsVn4lYcVdbWsmTXwSui4B5fx/view?usp=drive_link) |

> **Panduan Import ke GNS3:**
> 1.  **Untuk file `.bin` (Router):** Buka menu *Edit > Preferences > Dynamips > IOS Routers*, klik *New*, dan pilih file bin tersebut.
> 2.  **Untuk file `.bin` (Switch):** Buka menu *Edit > Preferences > IOS on UNIX > IOU Devices*, klik *New*, dan pilih file bin tersebut.
> 3.  **Untuk file `.zip` (Cisco ASAv):** Buka menu *File > Import Appliance*, lalu pilih file zip tersebut. Ikuti wizard instalasi GNS3.

---

## 2. Arsitektur Jaringan

Sistem ini membagi jaringan menjadi 5 zona keamanan:

<img width="1149" height="645" alt="Topologi Gns3" src="https://github.com/user-attachments/assets/2bf9f3b4-b0ac-4ebd-ba82-ad19d3a3c2f4" />

1.  **Internet (WAN):** Koneksi ke dunia luar via NAT.
2.  **Server Zone (`10.0`):** Tempat aplikasi disimpan.
3.  **Local Zone (`20.0`):** Klien karyawan tepercaya.
4.  **Guest Zone (`30.0`):** Klien tamu (akses terbatas).
5.  **External Zone (`172.16`):** Klien publik/internet (diblokir firewall).

---

## 3. Instalasi Infrastruktur (GNS3)

<details>
<summary><strong>Klik untuk melihat langkah-langkah setup GNS3</strong></summary>

1.  **Install GNS3 & GNS3 VM:** Ikuti wizard instalasi. Pastikan GNS3 VM berjalan di VirtualBox dan terhubung (lampu hijau di GNS3).
    
2.  **Buat Template VM (Host):**
    * Di GNS3, buka `Edit > Preferences > VirtualBox VMs`.
    * Klik `New`, lalu buat VM baru menggunakan ISO (Alpine, Ubuntu, Lubuntu).
    * *Tips:* Untuk Alpine Router, set Network Adapters menjadi **5**.

3.  **Bangun Topologi:**
    * Tarik node **NAT** (Internet).
    * Tarik node **Alpine Linux** (Router Pusat).
    * Tarik node **Switch** (Gunakan Cisco IOU L2 atau Ethernet Switch bawaan) dan hubungkan ke VM.

4.  **Koneksi Kabel:**
    * `eth0` Alpine -> NAT
    * `eth1` Alpine -> Switch Server -> Ubuntu
    * `eth2` Alpine -> Switch Lokal -> Lubuntu 1
    * `eth3` Alpine -> Switch Guest -> Lubuntu 2
    * `eth4` Alpine -> Switch External -> Lubuntu 3

</details>

---

## 4. Konfigurasi Router (Alpine Linux)

Ini adalah langkah paling krusial untuk mengubah Alpine Linux menjadi Router, Firewall, dan VPN Server.

<details>
<summary><strong>A. Instalasi Sistem Operasi (Wajib Baca)</strong></summary>

Sebelum melakukan konfigurasi jaringan, Anda harus menginstal OS Alpine Linux ke dalam VM VirtualBox Anda.

**Panduan Instalasi:**
Ikuti tutorial langkah demi langkah pada link berikut untuk menginstal Alpine Linux:
👉 **[Tutorial Instalasi Alpine Linux di VirtualBox (itsfoss.com)](https://itsfoss.com/alpine-linux-virtualbox/)**

> ⚠️ **PERINGATAN PENTING:**
> Ikuti tutorial tersebut **HANYA SAMPAI STEP 4 (Post-install set up)**.
>
> * **Lakukan:** Install Nano editor dan Enable community repositories (sesuai Step 4).
> * **JANGAN LAKUKAN:** Langkah selanjutnya yang menyuruh menginstal Desktop Environment (XFCE/GNOME). Router kita harus berbasis teks (CLI) agar ringan dan cepat.
> * Setelah selesai Step 4 (mengedit `/etc/apk/repositories`), kembalilah ke panduan ini untuk langkah **B. Login & Instalasi Paket**.

</details>

<details>
<summary><strong>B. Login & Instalasi Paket Jaringan</strong></summary>

1.  Nyalakan Alpine Linux. Login sebagai `root` (tanpa password).
2.  Pastikan terhubung internet (GNS3 NAT).
3.  Jalankan perintah ini untuk mengupdate dan menginstall paket:
    ```bash
    apk update
    apk add nano bash iptables dnsmasq openvpn easy-rsa python3
    ```
</details>

<details>
<summary><strong>C. Konfigurasi IP & Routing</strong></summary>

1.  **Aktifkan IP Forwarding** (Agar bisa jadi router):
    ```bash
    nano /etc/sysctl.conf
    # Hapus tanda pagar (#) pada baris: net.ipv4.ip_forward=1
    # Simpan (Ctrl+O, Enter, Ctrl+X)
    sysctl -p
    ```

2.  **Konfigurasi Interface:**
    Buka file `nano /etc/network/interfaces`, hapus isinya, ganti dengan:
    *(Pastikan konfigurasi ini sesuai dengan topologi kabel GNS3 Anda)*
    ```ini
    auto lo
    iface lo inet loopback

    # WAN (Internet dari GNS3 NAT)
    auto eth0
    iface eth0 inet dhcp

    # Server Zone
    auto eth1
    iface eth1 inet static
        address 192.168.10.1
        netmask 255.255.255.0

    # Local Zone
    auto eth2
    iface eth2 inet static
        address 192.168.20.1
        netmask 255.255.255.0

    # Guest Zone
    auto eth3
    iface eth3 inet static
        address 192.168.30.1
        netmask 255.255.255.0

    # External Zone
    auto eth4
    iface eth4 inet static
        address 172.16.1.1
        netmask 255.255.255.0
    ```
    Restart network: `rc-service networking restart`
</details>

<details>
<summary><strong>D. Konfigurasi DHCP Server</strong></summary>

Buka file `nano /etc/dnsmasq.conf`, isi dengan:
```ini
bind-interfaces
# Interface yang dilayani
interface=eth1
interface=eth2
interface=eth3

# Rentang IP (Ranges)
dhcp-range=interface:eth1,192.168.10.100,192.168.10.150,255.255.255.0,12h
dhcp-range=interface:eth2,192.168.20.100,192.168.20.150,255.255.255.0,12h
dhcp-range=interface:eth3,192.168.30.100,192.168.30.150,255.255.255.0,12h

# Gateway & DNS Options
dhcp-option=interface:eth1,option:router,192.168.10.1
dhcp-option=interface:eth2,option:router,192.168.20.1
dhcp-option=interface:eth3,option:router,192.168.30.1
dhcp-option=option:dns-server,8.8.8.8
