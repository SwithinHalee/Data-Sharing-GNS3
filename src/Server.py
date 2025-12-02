import socketserver
import os
import threading

# --- KONFIGURASI SERVER ---
HOST = '0.0.0.0'    # Mendengarkan di semua interface (Lokal & VPN)
PORT = 50001        # Port yang dibuka di Firewall
SHARE_DIR = "share" # Folder penyimpanan file
BUFFER = 4096       # Ukuran buffer transfer data

class ClientHandler(socketserver.BaseRequestHandler):
    """Class Handler: Menangani satu koneksi klien dalam thread terpisah"""

    def handle(self):
        addr = self.client_address
        print(f"[+] Koneksi masuk dari: {addr}")

        try:
            while True:
                # 1. Menerima data perintah mentah
                data = self.request.recv(1024).strip().decode()
                if not data: break # Jika data kosong, klien putus koneksi

                # 2. Memecah perintah (Format: PERINTAH|ARGUMEN)
                parts = data.split('|', 1)
                cmd = parts[0].upper()

                # --- LOGIKA IF/ELSE UNTUK SETIAP PERINTAH ---

                # [A] FITUR LIST FILE
                if cmd == "LIST":
                    files = os.listdir(SHARE_DIR)
                    # Menggabungkan nama file dengan titik koma (;) agar dikirim satu baris
                    msg = ";".join(files) if files else "Folder kosong"
                    self.request.sendall(f"OK|{msg}\n".encode())

                # [B] FITUR UPLOAD (Terima file dari Klien)
                elif cmd == "UPLOAD":
                    filename = os.path.basename(parts[1]) # Ambil nama file saja (keamanan)
                    filepath = os.path.join(SHARE_DIR, filename)
                    
                    # Beritahu klien server siap
                    self.request.sendall(b"READY\n")
                    
                    # Terima ukuran file
                    filesize = int(self.request.recv(1024).strip())
                    
                    # Loop penerimaan data
                    with open(filepath, 'wb') as f:
                        received = 0
                        while received < filesize:
                            chunk = self.request.recv(BUFFER)
                            f.write(chunk)
                            received += len(chunk)
                    self.request.sendall(b"OK|Upload Selesai\n")

                # [C] FITUR DOWNLOAD (Kirim file ke Klien)
                elif cmd == "DOWNLOAD":
                    filename = os.path.basename(parts[1])
                    filepath = os.path.join(SHARE_DIR, filename)

                    if os.path.exists(filepath):
                        # Kirim ukuran file
                        size = os.path.getsize(filepath)
                        self.request.sendall(f"OK|{size}\n".encode())
                        
                        # Baca file dan kirim
                        with open(filepath, 'rb') as f:
                            while True:
                                chunk = f.read(BUFFER)
                                if not chunk: break
                                self.request.sendall(chunk)
                    else:
                        self.request.sendall(b"ERROR|File tidak ditemukan\n")
                
                # [D] FITUR DELETE (Hapus File)
                elif cmd == "DELETE":
                    filename = os.path.basename(parts[1])
                    filepath = os.path.join(SHARE_DIR, filename)
                    
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                            self.request.sendall(b"OK|File berhasil dihapus\n")
                        except Exception as e:
                            self.request.sendall(f"ERROR|Gagal menghapus: {e}\n".encode())
                    else:
                        self.request.sendall(b"ERROR|File tidak ditemukan\n")
                
                else:
                    print(f"[-] Perintah tidak dikenal dari {addr}")

        except Exception as e:
            print(f"[-] Error koneksi {addr}: {e}")
        
        print(f"[-] Koneksi ditutup: {addr}")

# --- CLASS SERVER UTAMA (MULTITHREADED) ---
class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Mengaktifkan Multithreading agar bisa banyak klien sekaligus"""
    pass

if __name__ == "__main__":
    # Buat folder jika belum ada
    if not os.path.exists(SHARE_DIR):
        os.makedirs(SHARE_DIR)
        print(f"[+] Folder '{SHARE_DIR}' siap.")
    
    # FIX PENTING: Mencegah error "Address already in use"
    socketserver.TCPServer.allow_reuse_address = True
    
    # Jalankan Server
    server = ThreadedServer((HOST, PORT), ClientHandler)
    print(f"[*] Server Data Sharing berjalan di {HOST}:{PORT}")
    print("[*] Tekan Ctrl+C untuk berhenti.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server dimatikan.")
        server.shutdown()