import socket
import os
import sys
import time # Penting untuk sinkronisasi upload

BUFFER = 4096

def receive_line(sock):
    """Fungsi bantu: Menerima data sampai ketemu baris baru (Enter)"""
    data = b""
    while True:
        chunk = sock.recv(1)
        if not chunk or chunk == b'\n':
            break
        data += chunk
    return data.decode()

def main():
    sock = None # Variabel untuk menyimpan status koneksi

    while True:
        # Prompt dinamis (menunjukkan status koneksi)
        prompt = "cli> " if sock else "cli (disconnected)> "
        
        try:
            cmd_input = input(prompt).strip()
        except EOFError:
            break # Handle Ctrl+D

        if not cmd_input: continue

        parts = cmd_input.split()
        cmd = parts[0].lower()

        try:
            # --- LOGIKA IF/ELSE PERINTAH KLIEN ---

            # [1] EXIT
            if cmd == "exit":
                break

            # [2] CONNECT
            elif cmd == "connect":
                if len(parts) != 3:
                    print("Usage: connect <ip> <port>")
                    continue
                
                # Reset socket lama jika ada
                if sock: sock.close()
                
                ip, port = parts[1], int(parts[2])
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                print(f"[+] Berhasil terhubung ke {ip}:{port}")
                continue 

            # Cek Koneksi sebelum menjalankan perintah lain
            elif not sock:
                print("[!] Belum terhubung. Gunakan: connect <ip> <port>")
                continue

            # [3] LIST
            elif cmd == "list":
                sock.sendall(b"LIST\n")
                resp = receive_line(sock)
                
                # Parsing respons (OK|file1;file2)
                parts_resp = resp.split('|', 1)
                if len(parts_resp) > 1:
                    # Ganti titik koma (;) dengan Enter (\n) untuk tampilan rapi
                    file_list = parts_resp[1].replace(';', '\n')
                    print(f"--- File di Server ---\n{file_list}\n----------------------")
                else:
                    print(resp)

            # [4] UPLOAD
            elif cmd == "upload":
                if len(parts) != 2:
                    print("Usage: upload <nama_file_lokal>")
                    continue
                
                local_file = parts[1]
                if not os.path.exists(local_file):
                    print("[!] File lokal tidak ditemukan.")
                    continue
                
                # Kirim Header
                sock.sendall(f"UPLOAD|{local_file}\n".encode())
                
                # FIX PENTING: Jeda sedikit agar server siap menerima ukuran
                time.sleep(0.1) 
                
                if receive_line(sock) == "READY":
                    size = os.path.getsize(local_file)
                    sock.sendall(f"{size}\n".encode()) # Kirim ukuran
                    
                    # Baca file dan kirim
                    with open(local_file, 'rb') as f:
                        while True:
                            chunk = f.read(BUFFER)
                            if not chunk: break
                            sock.sendall(chunk)
                    
                    print(f"Server: {receive_line(sock)}") # Terima OK

            # [5] DOWNLOAD
            elif cmd == "download":
                if len(parts) < 2:
                    print("Usage: download <nama_file_server>")
                    continue
                
                remote_file = parts[1]
                sock.sendall(f"DOWNLOAD|{remote_file}\n".encode())
                
                resp = receive_line(sock)
                status, payload = resp.split('|', 1)

                if status == "OK":
                    size = int(payload)
                    received = 0
                    print(f"[*] Mendownload {remote_file} ({size} bytes)...")
                    
                    with open(remote_file, 'wb') as f:
                        while received < size:
                            chunk = sock.recv(BUFFER)
                            f.write(chunk)
                            received += len(chunk)
                    print(f"[+] Download sukses.")
                else:
                    print(f"[!] Server Error: {payload}")
            
            # [6] DELETE
            elif cmd == "delete":
                if len(parts) != 2:
                    print("Usage: delete <nama_file_server>")
                    continue
                remote_file = parts[1]
                sock.sendall(f"DELETE|{remote_file}\n".encode())
                print(f"Server: {receive_line(sock)}")

            # [7] HELP
            elif cmd == "help":
                print("--- Bantuan ---")
                print("connect <ip> <port> : Hubungkan ke server")
                print("list                : Lihat file di server")
                print("upload <file>       : Upload file lokal")
                print("download <file>     : Download file server")
                print("delete <file>       : Hapus file di server")
                print("exit                : Keluar")

            else:
                print(f"Perintah '{cmd}' tidak dikenal. Ketik 'help'.")

        except Exception as e:
            print(f"[!] Error: {e}")
            sock = None # Reset koneksi jika error fatal

    if sock: sock.close()
    print("[*] Program selesai.")

if __name__ == "__main__":
    main()