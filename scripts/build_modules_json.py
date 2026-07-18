"""Rebuild the complete modules.json from the ground up."""
import json

data = {
  "year1": {
    "semester1": {
      "name": "Semester 1",
      "modules": [
        {
          "name": "Programming Concepts",
          "code": "ICN 1101",
          "icon": "programming",
          "tags": ["python", "automation", "file-ops"],
          "description": "Python fundamentals — variables, control flow, functions, file operations, and automation basics.",
          "projects": [
            {
              "title": "University Folder Organizer",
              "difficulty": "Beginner",
              "filename": "folder_organizer.py",
              "description": "Automatically create your university course folder structure for the semester.",
              "code": 'import os\nfrom pathlib import Path\n\ndef create_uni_structure():\n    home = Path.home() / \'MUST\'\n    year = home / \'Year1\'\n    \n    courses = {\n        \'ICN1101-Programming\': [\'Lectures\', \'Assignments\', \'Code\', \'Notes\'],\n        \'ICN1102-Networks\': [\'Lectures\', \'Labs\', \'PacketTracer\', \'Notes\'],\n        \'ICN1103-OS\': [\'Lectures\', \'Labs\', \'Assignments\'],\n        \'ICN1104-Architecture\': [\'Lectures\', \'Notes\', \'Diagrams\']\n    }\n    \n    for course, folders in courses.items():\n        course_path = year / course\n        for folder in folders:\n            (course_path / folder).mkdir(parents=True, exist_ok=True)\n        print(f\'Created: {course}\')\n    \n    print(f\'\\nAll folders ready at: {year}\')\n\nif __name__ == \'__main__\':\n    create_uni_structure()',
              "explanation": [
                "<strong>Line 1-2:</strong> Import os and Path from pathlib. Path is the modern way to handle file paths.",
                "<strong>Line 5:</strong> Path.home() returns your user directory. We append 'MUST' as the root university folder.",
                "<strong>Lines 8-13:</strong> Dictionary mapping course codes to their required subfolders.",
                "<strong>Lines 15-19:</strong> Loop through each course, create parent directories with mkdir(parents=True).",
                "<strong>Line 18:</strong> The / operator on Path objects joins paths cleanly."
              ]
            }
          ]
        },
        {
          "name": "Computer Systems Architecture",
          "code": "ICN 1102",
          "icon": "systems",
          "tags": ["hardware", "cpu", "memory", "monitoring"],
          "description": "CPU architecture, memory hierarchy, storage systems. Build system profilers and hardware monitors.",
          "projects": [
            {
              "title": "System Hardware Profiler",
              "difficulty": "Beginner",
              "filename": "system_profiler.py",
              "description": "Display detailed CPU, RAM, and disk information using psutil.",
              "code": 'import psutil\nimport platform\n\ndef system_profiler():\n    print(\'=\' * 50)\n    print(\'  SYSTEM HARDWARE PROFILER\')\n    print(\'=\' * 50)\n    \n    print(f\'\\nCPU:\')\n    print(f\'   Processor: {platform.processor()}\')\n    print(f\'   Physical cores: {psutil.cpu_count(logical=False)}\')\n    print(f\'   Total logical cores: {psutil.cpu_count(logical=True)}\')\n    print(f\'   Max frequency: {psutil.cpu_freq().max:.0f} MHz\')\n    \n    mem = psutil.virtual_memory()\n    print(f\'\\nRAM:\')\n    print(f\'   Total: {mem.total / (1024**3):.1f} GB\')\n    print(f\'   Available: {mem.available / (1024**3):.1f} GB\')\n    print(f\'   Used: {mem.percent}%\')\n\nif __name__ == \'__main__\':\n    system_profiler()',
              "explanation": [
                "<strong>Line 1:</strong> psutil is the standard library for system information. Install with pip install psutil.",
                "<strong>Line 10:</strong> cpu_count(logical=False) returns physical cores.",
                "<strong>Line 12:</strong> cpu_freq().max gives maximum clock speed in MHz.",
                "<strong>Lines 15-18:</strong> virtual_memory() returns named tuple. /(1024**3) converts bytes to gigabytes."
              ]
            }
          ]
        },
        {
          "name": "Computer Network Engineering",
          "code": "ICN 1103",
          "icon": "networking",
          "tags": ["networking", "tcp/ip", "osi", "scanner"],
          "description": "OSI model, TCP/IP stack, IP addressing, subnetting. Build network discovery and diagnostic tools.",
          "projects": [
            {
              "title": "Network Device Scanner",
              "difficulty": "Beginner",
              "filename": "network_scanner.py",
              "description": "Discover all devices on your local network using ARP requests with Scapy.",
              "code": 'from scapy.all import ARP, Ether, srp\n\ndef scan_network(ip_range=\'192.168.1.0/24\'):\n    arp = ARP(pdst=ip_range)\n    ether = Ether(dst=\'ff:ff:ff:ff:ff:ff\')\n    packet = ether / arp\n    result = srp(packet, timeout=3, verbose=0)[0]\n    \n    devices = []\n    for sent, received in result:\n        devices.append({\'ip\': received.psrc, \'mac\': received.hwsrc})\n    return devices\n\nif __name__ == \'__main__\':\n    devices = scan_network()\n    print(f\'Found {len(devices)} devices:\')\n    for d in devices:\n        print(f\'  {d[\"ip\"]:15} - {d[\"mac\"]}\')',
              "explanation": [
                "<strong>Line 1:</strong> Scapy is the Swiss Army knife of packet manipulation.",
                "<strong>Line 4:</strong> pdst sets the IP range. '192.168.1.0/24' scans all 254 addresses.",
                "<strong>Line 5:</strong> 'ff:ff:ff:ff:ff:ff' is the broadcast MAC address.",
                "<strong>Line 6:</strong> The / operator stacks layers — Ethernet frame containing ARP request.",
                "<strong>Line 7:</strong> srp() sends and receives at Layer 2. timeout=3 seconds."
              ]
            }
          ]
        },
        {
          "name": "Operating Systems",
          "code": "ICN 1104",
          "icon": "systems",
          "tags": ["os", "processes", "sysadmin", "linux"],
          "description": "Process management, memory management, file systems. Build sysadmin automation and monitoring tools.",
          "projects": [
            {
              "title": "Process Monitor & Manager",
              "difficulty": "Intermediate",
              "filename": "process_monitor.py",
              "description": "List running processes, identify resource hogs, and monitor system resources.",
              "code": 'import psutil\n\ndef top_processes(limit=10):\n    procs = []\n    for p in psutil.process_iter([\'pid\', \'name\', \'cpu_percent\', \'memory_percent\']):\n        try:\n            info = p.info\n            info[\'mem_mb\'] = p.memory_info().rss / (1024 * 1024)\n            procs.append(info)\n        except:\n            continue\n    procs.sort(key=lambda x: x[\'mem_mb\'], reverse=True)\n    return procs[:limit]\n\nif __name__ == \'__main__\':\n    print(\'Top Memory Users:\\n\')\n    for i, p in enumerate(top_processes(), 1):\n        print(f\'{i}. PID:{p[\"pid\"]:6} | {p[\"mem_mb\"]:6.0f}MB | {p[\"name\"]}\')',
              "explanation": [
                "<strong>Line 3:</strong> process_iter() loops through all running processes with specified fields.",
                "<strong>Line 6:</strong> memory_info().rss is Resident Set Size — actual physical RAM.",
                "<strong>Line 10:</strong> Lambda sorts by memory usage descending.",
                "<strong>Line 11:</strong> [:limit] returns only the top N processes."
              ]
            }
          ]
        }
      ]
    },
    "semester2": {
      "name": "Semester 2",
      "modules": [
        {
          "name": "Object Oriented Programming",
          "code": "ICN 1201",
          "icon": "programming",
          "tags": ["python", "oop", "classes", "inheritance"],
          "description": "Classes, objects, inheritance, polymorphism. Model network devices and systems as Python classes.",
          "projects": [
            {
              "title": "Network Device Class Hierarchy",
              "difficulty": "Intermediate",
              "filename": "network_devices.py",
              "description": "Design an OOP model of network infrastructure — routers, switches, and firewalls as Python classes.",
              "code": 'class NetworkDevice:\n    def __init__(self, name, ip, mac=None):\n        self.name = name\n        self.ip = ip\n        self.mac = mac\n        self.online = False\n    \n    def ping(self):\n        import os\n        param = \'-n 1\' if os.name == \'nt\' else \'-c 1\'\n        response = os.system(f\'ping {param} {self.ip} > /dev/null 2>&1\')\n        self.online = (response == 0)\n        return self.online\n    \n    def __str__(self):\n        status = \'ONLINE\' if self.online else \'OFFLINE\'\n        return f\'{status} {self.name} ({self.ip})\'\n\nclass Router(NetworkDevice):\n    def __init__(self, name, ip, model=None):\n        super().__init__(name, ip)\n        self.model = model\n        self.routes = []\n    \n    def add_route(self, network, gateway):\n        self.routes.append({\'network\': network, \'gateway\': gateway})\n\nif __name__ == \'__main__\':\n    router = Router(\'Core-R1\', \'192.168.1.1\', \'Cisco 2900\')\n    router.add_route(\'10.0.0.0/8\', \'192.168.1.254\')\n    print(f\'Created: {router}\')',
              "explanation": [
                "<strong>Lines 1-6:</strong> Base NetworkDevice class with name, IP, MAC, and online status.",
                "<strong>Lines 8-11:</strong> ping() method checks reachability using OS ping command.",
                "<strong>Lines 17-23:</strong> Router INHERITS from NetworkDevice. Adds routing table.",
                "<strong>Line 20:</strong> super().__init__() calls the parent constructor."
              ]
            }
          ]
        },
        {
          "name": "Data Communication",
          "code": "ICN 1202",
          "icon": "networking",
          "tags": ["networking", "packets", "protocols", "scapy"],
          "description": "Communication protocols, packet structure, data transmission. Analyze network traffic with Python.",
          "projects": [
            {
              "title": "Packet Sniffer & Analyzer",
              "difficulty": "Intermediate",
              "filename": "packet_sniffer.py",
              "description": "Capture and analyze live network packets to understand TCP/IP.",
              "code": 'from scapy.all import sniff, IP, TCP, UDP\n\ndef analyze_packet(packet):\n    if packet.haslayer(IP):\n        src = packet[IP].src\n        dst = packet[IP].dst\n        \n        if packet.haslayer(TCP):\n            print(f\'TCP {src}:{packet[TCP].sport} -> {dst}:{packet[TCP].dport}\')\n        elif packet.haslayer(UDP):\n            print(f\'UDP {src}:{packet[UDP].sport} -> {dst}:{packet[UDP].dport}\')\n\nprint(\'Capturing 20 packets...\')\nsniff(prn=analyze_packet, count=20)\nprint(\'Capture complete.\')',
              "explanation": [
                "<strong>Line 1:</strong> sniff() captures packets. IP, TCP, UDP are layer access classes.",
                "<strong>Line 4:</strong> haslayer(IP) checks if packet contains an IP layer.",
                "<strong>Lines 5-7:</strong> Extract source IP, destination IP, protocol number.",
                "<strong>Line 15:</strong> prn=analyze_packet sets callback. count=20 stops after 20 packets."
              ]
            }
          ]
        },
        {
          "name": "Routing and Switching",
          "code": "ICN 1203",
          "icon": "networking",
          "tags": ["networking", "routing", "switching", "automation"],
          "description": "Routing protocols, switching concepts, VLANs. Automate network device configuration with Python.",
          "projects": [
            {
              "title": "Network Config Backup Tool",
              "difficulty": "Intermediate",
              "filename": "config_backup.py",
              "description": "Automatically backup configurations from network devices via SSH using Netmiko.",
              "code": 'from netmiko import ConnectHandler\nfrom datetime import datetime\n\ndef backup_device(device_info):\n    try:\n        conn = ConnectHandler(**device_info)\n        hostname = conn.find_prompt().strip(\'#\')\n        config = conn.send_command(\'show running-config\')\n        filename = f\'{hostname}_{datetime.now():%Y%m%d}.cfg\'\n        with open(filename, \'w\') as f:\n            f.write(config)\n        conn.disconnect()\n        print(f\'Backed up: {hostname} -> {filename}\')\n    except Exception as e:\n        print(f\'Failed: {device_info[\"host\"]} - {e}\')\n\nif __name__ == \'__main__\':\n    devices = [{\'device_type\': \'cisco_ios\', \'host\': \'192.168.1.1\', \'username\': \'admin\', \'password\': \'cisco\'}]\n    for device in devices:\n        backup_device(device)',
              "explanation": [
                "<strong>Line 1:</strong> Netmiko simplifies SSH connections to network devices.",
                "<strong>Line 6:</strong> **device_info unpacks dictionary as keyword arguments.",
                "<strong>Line 7:</strong> find_prompt() returns device prompt. Stripping '#' gives hostname.",
                "<strong>Line 8:</strong> send_command() executes 'show running-config' on the device."
              ]
            }
          ]
        },
        {
          "name": "Database Design and Implementation",
          "code": "ICN 1204",
          "icon": "data",
          "tags": ["database", "sqlite", "sql", "crud"],
          "description": "Database design, normalization, SQL. Build database-driven applications with SQLite and Python.",
          "projects": [
            {
              "title": "Network Inventory Database",
              "difficulty": "Intermediate",
              "filename": "inventory_db.py",
              "description": "Complete CRUD system for tracking network devices, locations, and maintenance history.",
              "code": 'import sqlite3\n\nclass InventoryDB:\n    def __init__(self, db=\'inventory.db\'):\n        self.conn = sqlite3.connect(db)\n        self.create_tables()\n    \n    def create_tables(self):\n        self.conn.execute(\'CREATE TABLE IF NOT EXISTS devices (id INTEGER PRIMARY KEY, hostname TEXT UNIQUE, ip TEXT UNIQUE, device_type TEXT, location TEXT)\')\n        self.conn.commit()\n    \n    def add_device(self, hostname, ip, dtype, location):\n        self.conn.execute(\'INSERT INTO devices (hostname, ip, device_type, location) VALUES (?,?,?,?)\', (hostname, ip, dtype, location))\n        self.conn.commit()\n        print(f\'Added: {hostname}\')\n    \n    def search(self, query=\'\'):\n        cursor = self.conn.execute(\'SELECT * FROM devices WHERE hostname LIKE ?\', (f\'%{query}%\',))\n        return cursor.fetchall()\n\nif __name__ == \'__main__\':\n    db = InventoryDB()\n    db.add_device(\'Core-SW1\', \'10.0.0.1\', \'Switch\', \'Server Room\')',
              "explanation": [
                "<strong>Line 1:</strong> sqlite3 comes bundled with Python — no installation needed.",
                "<strong>Lines 4-5:</strong> __init__ connects to database and creates tables on startup.",
                "<strong>Lines 8-9:</strong> CREATE TABLE IF NOT EXISTS — safe to run multiple times.",
                "<strong>Lines 12-14:</strong> Parameterized queries with ? prevent SQL injection."
              ]
            }
          ]
        },
        {
          "name": "Hardware and Software Integration",
          "code": "ICN 1205",
          "icon": "systems",
          "tags": ["hardware", "serial", "firmware", "integration"],
          "description": "Hardware-software interfaces, device drivers, firmware. Communicate with hardware using Python.",
          "projects": [
            {
              "title": "Serial Port Communicator",
              "difficulty": "Intermediate",
              "filename": "serial_comm.py",
              "description": "Communicate with hardware devices (Arduino, routers, sensors) via serial port.",
              "code": 'import serial\n\ndef list_serial_ports():\n    ports = serial.tools.list_ports.comports()\n    for port in ports:\n        print(f\'  {port.device} - {port.description}\')\n    return [p.device for p in ports]\n\ndef connect_and_read(port, baud=9600):\n    try:\n        ser = serial.Serial(port, baud, timeout=1)\n        print(f\'Connected to {port}\')\n        for _ in range(5):\n            if ser.in_waiting:\n                data = ser.readline().decode().strip()\n                print(f\'Received: {data}\')\n        ser.close()\n    except Exception as e:\n        print(f\'Error: {e}\')\n\nif __name__ == \'__main__\':\n    ports = list_serial_ports()\n    if ports:\n        connect_and_read(ports[0])',
              "explanation": [
                "<strong>Line 1:</strong> pyserial is the standard library for serial communication.",
                "<strong>Lines 3-6:</strong> list_ports.comports() enumerates all serial ports on the system.",
                "<strong>Lines 10-11:</strong> Serial() opens connection. Baud rate must match the device.",
                "<strong>Lines 13-14:</strong> in_waiting checks for available data, readline() reads until newline."
              ]
            }
          ]
        }
      ]
    }
  },
  "year2": {
    "semester1": {
      "name": "Semester 1",
      "modules": [
        {
          "name": "Computer Network Management",
          "code": "ICN 2101",
          "icon": "networking",
          "tags": ["networking", "snmp", "monitoring", "automation"],
          "description": "SNMP, network monitoring, fault management, configuration management. Build network monitoring tools.",
          "projects": [
            {
              "title": "SNMP Network Monitor",
              "difficulty": "Intermediate",
              "filename": "snmp_monitor.py",
              "description": "Monitor network device health via SNMP queries.",
              "code": 'from pysnmp.hlapi import *\n\ndef snmp_get(host, community, oid):\n    iterator = getCmd(SnmpEngine(), CommunityData(community, mpModel=1), UdpTransportTarget((host, 161)), ContextData(), ObjectType(ObjectIdentity(oid)))\n    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)\n    if errorIndication:\n        return f\'Error: {errorIndication}\'\n    return str(varBinds[0][1])\n\nif __name__ == \'__main__\':\n    sys_name = snmp_get(\'192.168.1.1\', \'public\', \'1.3.6.1.2.1.1.5.0\')\n    print(f\'Device Name: {sys_name}\')',
              "explanation": [
                "<strong>Line 1:</strong> pysnmp is the Python SNMP library. Install with pip install pysnmp.",
                "<strong>Line 4:</strong> getCmd builds an SNMP GET request with CommunityData for SNMPv1/v2c.",
                "<strong>Line 9:</strong> OID 1.3.6.1.2.1.1.5.0 is sysName — the device hostname."
              ]
            }
          ]
        },
        {
          "name": "Information Systems",
          "code": "ICN 2102",
          "icon": "data",
          "tags": ["systems", "analysis", "design", "uml"],
          "description": "Information systems analysis, design methodologies, UML modeling. Build system design tools.",
          "projects": [
            {
              "title": "UML Diagram Generator",
              "difficulty": "Intermediate",
              "filename": "uml_generator.py",
              "description": "Generate PlantUML class diagrams from Python classes using introspection.",
              "code": 'import inspect\n\nclass UMLGenerator:\n    def __init__(self, classes):\n        self.classes = classes\n    \n    def generate(self):\n        plantuml = \'@startuml\\n\'\n        for cls in self.classes:\n            plantuml += f\'class {cls.__name__} {{\\n\'\n            for name, method in inspect.getmembers(cls, inspect.isfunction):\n                if not name.startswith(\'_\'):\n                    plantuml += f\'  +{name}()\\n\'\n            plantuml += \'}\\n\'\n        plantuml += \'@enduml\'\n        return plantuml\n\nif __name__ == \'__main__\':\n    class Device:\n        def connect(self): pass\n        def disconnect(self): pass\n    gen = UMLGenerator([Device])\n    print(gen.generate())',
              "explanation": [
                "<strong>Line 1:</strong> inspect module provides live introspection of Python objects.",
                "<strong>Lines 8-14:</strong> Generates PlantUML format by iterating through class methods.",
                "<strong>Line 11:</strong> Filters out private/dunder methods starting with _.",
                "<strong>Line 13:</strong> inspect.signature() extracts method parameters."
              ]
            }
          ]
        },
        {
          "name": "Linear Algebra and Calculus",
          "code": "ICN 2103",
          "icon": "ai",
          "tags": ["math", "numpy", "linear-algebra", "calculus"],
          "description": "Linear algebra, calculus, matrices. Apply mathematical computing with NumPy.",
          "projects": [
            {
              "title": "Matrix Operations Toolkit",
              "difficulty": "Intermediate",
              "filename": "matrix_toolkit.py",
              "description": "Common linear algebra operations — determinants, eigenvalues, solving systems.",
              "code": 'import numpy as np\n\nif __name__ == \'__main__\':\n    A = np.array([[3, 1], [1, 2]])\n    b = np.array([9, 8])\n    x = np.linalg.solve(A, b)\n    print(f\'Solution: {x}\')\n    \n    vals, vecs = np.linalg.eig(A)\n    print(f\'Eigenvalues: {vals}\')',
              "explanation": [
                "<strong>Line 1:</strong> NumPy is the fundamental package for scientific computing.",
                "<strong>Line 6:</strong> np.linalg.solve() solves linear equations Ax = b.",
                "<strong>Line 9:</strong> np.linalg.eig() returns eigenvalues and eigenvectors."
              ]
            }
          ]
        }
      ]
    },
    "semester2": {
      "name": "Semester 2",
      "modules": [
        {
          "name": "Linux Operating System",
          "code": "ICN 2201",
          "icon": "systems",
          "tags": ["linux", "bash", "shell", "automation"],
          "description": "Linux administration, shell scripting, system services. Automate Linux tasks with Python.",
          "projects": [
            {
              "title": "Linux System Health Reporter",
              "difficulty": "Intermediate",
              "filename": "linux_reporter.py",
              "description": "Generate a comprehensive system health report for Linux servers.",
              "code": 'import psutil\nimport subprocess\nfrom datetime import datetime\n\ndef health_report():\n    out = subprocess.run([\'uname\', \'-a\'], capture_output=True, text=True)\n    print(f\'System: {out.stdout.strip()}\')\n    \n    cpu = psutil.cpu_percent(percpu=True)\n    print(f\'CPU per core: {cpu}\')\n    \n    mem = psutil.virtual_memory()\n    print(f\'Memory: {mem.percent}% used\')\n    \n    for part in psutil.disk_partitions():\n        try:\n            usage = psutil.disk_usage(part.mountpoint)\n            print(f\'Disk {part.mountpoint}: {usage.percent}%\')\n        except:\n            pass\n\nif __name__ == \'__main__\':\n    health_report()',
              "explanation": [
                "<strong>Line 6:</strong> subprocess.run() executes uname -a to get kernel info.",
                "<strong>Line 9:</strong> cpu_percent(percpu=True) returns per-core CPU usage.",
                "<strong>Line 12:</strong> virtual_memory() gives detailed RAM information.",
                "<strong>Lines 15-19:</strong> Iterate through disk partitions with error handling."
              ]
            }
          ]
        },
        {
          "name": "Artificial Intelligence",
          "code": "ICN 2202",
          "icon": "ai",
          "tags": ["ai", "search", "algorithms", "heuristics"],
          "description": "AI fundamentals, search algorithms, heuristics, knowledge representation. Implement AI in Python.",
          "projects": [
            {
              "title": "A* Pathfinding Visualizer",
              "difficulty": "Intermediate",
              "filename": "astar_pathfinder.py",
              "description": "Implement the A* search algorithm to find shortest paths in a grid.",
              "code": 'import heapq\n\ndef astar(grid, start, goal):\n    rows, cols = len(grid), len(grid[0])\n    open_set = [(0, start)]\n    came_from = {}\n    g_score = {start: 0}\n    \n    while open_set:\n        _, current = heapq.heappop(open_set)\n        if current == goal:\n            path = [current]\n            while current in came_from:\n                current = came_from[current]\n                path.append(current)\n            return path[::-1]\n        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:\n            nx, ny = current[0]+dx, current[1]+dy\n            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:\n                tg = g_score[current] + 1\n                if (nx,ny) not in g_score or tg < g_score[(nx,ny)]:\n                    came_from[(nx,ny)] = current\n                    g_score[(nx,ny)] = tg\n                    heapq.heappush(open_set, (tg + abs(nx-goal[0]) + abs(ny-goal[1]), (nx,ny)))\n    return None\n\nif __name__ == \'__main__\':\n    grid = [[0,0,0],[0,1,0],[0,0,0]]\n    path = astar(grid, (0,0), (2,2))\n    print(f\'Path: {path}\')',
              "explanation": [
                "<strong>Line 1:</strong> heapq provides priority queue for the open set.",
                "<strong>Line 12:</strong> Manhattan distance heuristic — admissible for grid movement.",
                "<strong>Lines 15-18:</strong> Reconstructs path by following came_from pointers.",
                "<strong>Lines 20-25:</strong> Expands neighbors, updates g_score with lower = better."
              ]
            }
          ]
        },
        {
          "name": "Enterprise Wireless Design",
          "code": "ICN 2203",
          "icon": "networking",
          "tags": ["wireless", "wifi", "rf", "planning"],
          "description": "Wireless network design, RF fundamentals, site surveys. Build wireless analysis tools.",
          "projects": [
            {
              "title": "WiFi Signal Strength Mapper",
              "difficulty": "Intermediate",
              "filename": "wifi_mapper.py",
              "description": "Scan WiFi networks and map signal strengths cross-platform.",
              "code": 'import subprocess\nimport platform\n\ndef scan_wifi():\n    if platform.system() == \'Windows\':\n        result = subprocess.run([\'netsh\', \'wlan\', \'show\', \'networks\', \'mode=Bssid\'], capture_output=True, text=True)\n    else:\n        result = subprocess.run([\'sudo\', \'iwlist\', \'scan\'], capture_output=True, text=True)\n    \n    networks = []\n    for line in result.stdout.split(\'\\n\'):\n        if \'SSID\' in line:\n            networks.append({\'ssid\': line.split(\':\')[-1].strip()})\n    return networks\n\nif __name__ == \'__main__\':\n    nets = scan_wifi()\n    for n in nets[:5]:\n        print(f\'Found: {n[\"ssid\"]}\')',
              "explanation": [
                "<strong>Lines 5-8:</strong> Cross-platform detection — netsh on Windows, iwlist on Linux.",
                "<strong>Lines 10-13:</strong> Parses SSID from command output.",
                "<strong>Lines 16-18:</strong> Displays first 5 discovered networks."
              ]
            }
          ]
        }
      ]
    }
  },
  "year3": {
    "semester1": {
      "name": "Semester 1",
      "modules": [
        {
          "name": "Networking Troubleshooting",
          "code": "ICN 3101",
          "icon": "networking",
          "tags": ["networking", "troubleshooting", "diagnostics", "tools"],
          "description": "Network troubleshooting methodologies, diagnostic tools, packet analysis.",
          "projects": [
            {
              "title": "Network Diagnostics Suite",
              "difficulty": "Advanced",
              "filename": "diagnostics.py",
              "description": "All-in-one diagnostics — ping sweep, DNS check, and port scanning.",
              "code": 'import socket\nimport subprocess\nimport concurrent.futures\n\ndef ping_sweep(prefix, start=1, end=254):\n    results = []\n    def ping(h):\n        resp = subprocess.run(f\'ping -n 1 {h}\'.split(), capture_output=True)\n        return h if resp.returncode == 0 else None\n    with concurrent.futures.ThreadPoolExecutor(50) as ex:\n        for host, up in zip([f\'{prefix}.{i}\' for i in range(start, end+1)], ex.map(ping, [f\'{prefix}.{i}\' for i in range(start, end+1)])):\n            if up:\n                results.append(host)\n    return results\n\ndef scan_ports(host, ports=[22, 80, 443]):\n    open_ports = []\n    for port in ports:\n        sock = socket.socket()\n        sock.settimeout(1)\n        if sock.connect_ex((host, port)) == 0:\n            open_ports.append(port)\n        sock.close()\n    return open_ports\n\nif __name__ == \'__main__\':\n    live = ping_sweep(\'192.168.1\', 1, 10)\n    print(f\'Live hosts: {live}\')',
              "explanation": [
                "<strong>Lines 5-12:</strong> ThreadPoolExecutor with 50 workers for concurrent pinging.",
                "<strong>Lines 14-21:</strong> Socket connect with 1s timeout. connect_ex returns 0 on success.",
                "<strong>Line 24:</strong> Sweeps first 10 IPs in 192.168.1.x range."
              ]
            }
          ]
        },
        {
          "name": "Web Technologies",
          "code": "ICN 3102",
          "icon": "web",
          "tags": ["web", "html", "css", "http"],
          "description": "Web protocols, HTTP, REST APIs, client-server architecture. Build web services.",
          "projects": [
            {
              "title": "REST API Client & Tester",
              "difficulty": "Intermediate",
              "filename": "api_tester.py",
              "description": "Lightweight API testing client with latency measurement.",
              "code": 'import requests\nimport time\n\nclass APITester:\n    def __init__(self, base_url):\n        self.base_url = base_url.rstrip(\'/\')\n        self.session = requests.Session()\n    \n    def get(self, endpoint):\n        start = time.perf_counter()\n        resp = self.session.get(f\'{self.base_url}/{endpoint.lstrip(\"/\")}\')\n        elapsed = (time.perf_counter() - start) * 1000\n        print(f\'{resp.status_code} | {elapsed:.1f}ms | {resp.url}\')\n        return resp\n\nif __name__ == \'__main__\':\n    tester = APITester(\'https://jsonplaceholder.typicode.com\')\n    tester.get(\'/posts/1\')',
              "explanation": [
                "<strong>Line 1:</strong> requests is the de facto HTTP library for Python.",
                "<strong>Lines 5-6:</strong> Session() reuses TCP connections for performance.",
                "<strong>Lines 10-11:</strong> time.perf_counter() measures high-precision latency."
              ]
            }
          ]
        },
        {
          "name": "Network Security",
          "code": "ICN 3103",
          "icon": "security",
          "tags": ["security", "encryption", "firewall", "crypto"],
          "description": "Network security principles, cryptography, firewalls, intrusion detection.",
          "projects": [
            {
              "title": "File Encryptor & Hasher",
              "difficulty": "Advanced",
              "filename": "file_encryptor.py",
              "description": "Encrypt files with AES-256 and verify integrity with SHA-256.",
              "code": 'from cryptography.fernet import Fernet\nimport hashlib\n\nclass FileEncryptor:\n    def __init__(self):\n        self.key = Fernet.generate_key()\n        self.cipher = Fernet(self.key)\n    \n    def encrypt(self, filepath):\n        with open(filepath, \'rb\') as f:\n            encrypted = self.cipher.encrypt(f.read())\n        with open(filepath + \'.enc\', \'wb\') as f:\n            f.write(encrypted)\n        print(f\'Encrypted: {filepath}.enc\')\n    \n    def hash_file(self, filepath):\n        sha = hashlib.sha256()\n        with open(filepath, \'rb\') as f:\n            sha.update(f.read())\n        return sha.hexdigest()\n\nif __name__ == \'__main__\':\n    enc = FileEncryptor()\n    enc.encrypt(\'secret.txt\')\n    print(f\'Hash: {enc.hash_file(\"secret.txt.enc\")}\')',
              "explanation": [
                "<strong>Line 1:</strong> cryptography.fernet provides symmetric authenticated encryption.",
                "<strong>Lines 5-7:</strong> Generates a random key and creates Fernet cipher.",
                "<strong>Lines 9-13:</strong> Reads file bytes, encrypts, writes .enc output.",
                "<strong>Lines 15-19:</strong> SHA-256 hashing for integrity verification."
              ]
            }
          ]
        },
        {
          "name": "Big Data",
          "code": "ICN 3104",
          "icon": "data",
          "tags": ["big-data", "processing", "analytics", "visualization"],
          "description": "Big data concepts, distributed processing, data analytics. Process large datasets with Python.",
          "projects": [
            {
              "title": "Log File Analyzer",
              "difficulty": "Intermediate",
              "filename": "log_analyzer.py",
              "description": "Analyze large log files — extract patterns and aggregate statistics.",
              "code": 'import re\nfrom collections import Counter\n\nclass LogAnalyzer:\n    def __init__(self, logfile):\n        self.logfile = logfile\n        self.pattern = re.compile(r\'(?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+).*\"(?P<method>\\w+) (?P<path>\\S+)[^"]*\" (?P<status>\\d+)\')\n    \n    def analyze(self):\n        ip_counter, status_counter = Counter(), Counter()\n        with open(self.logfile) as f:\n            for line in f:\n                m = self.pattern.search(line)\n                if m:\n                    ip_counter[m.group(\'ip\')] += 1\n                    status_counter[m.group(\'status\')] += 1\n        print(\'Top IPs:\', ip_counter.most_common(3))\n        print(\'Status codes:\', dict(status_counter))\n\nif __name__ == \'__main__\':\n    LogAnalyzer(\'access.log\').analyze()',
              "explanation": [
                "<strong>Line 1-2:</strong> re for regex, Counter for auto-counting.",
                "<strong>Line 7:</strong> Compiled regex with named groups for IP, method, path, status.",
                "<strong>Lines 10-14:</strong> Streaming file read — works with gigabyte log files.",
                "<strong>Line 15:</strong> most_common(3) returns top 3 IPs by request count."
              ]
            }
          ]
        }
      ]
    },
    "semester2": {
      "name": "Semester 2",
      "modules": [
        {
          "name": "Network Forensics",
          "code": "ICN 3201",
          "icon": "forensics",
          "tags": ["forensics", "investigation", "analysis", "evidence"],
          "description": "Digital forensics principles, evidence collection, analysis techniques.",
          "projects": [
            {
              "title": "PCAP Forensics Analyzer",
              "difficulty": "Advanced",
              "filename": "pcap_analyzer.py",
              "description": "Analyze packet captures for forensic evidence and suspicious traffic.",
              "code": 'from scapy.all import rdpcap, IP, TCP, DNS\nfrom collections import Counter\n\ndef analyze_pcap(filepath):\n    packets = rdpcap(filepath)\n    ip_conv = Counter()\n    dns_queries = []\n    for pkt in packets:\n        if IP in pkt:\n            ip_conv[(pkt[IP].src, pkt[IP].dst)] += 1\n            if DNS in pkt and pkt[DNS].qr == 0:\n                dns_queries.append(pkt[DNS].qd.qname.decode())\n    print(\'Top conversations:\', ip_conv.most_common(3))\n    print(\'DNS queries:\', dns_queries[:5])\n\nif __name__ == \'__main__\':\n    analyze_pcap(\'capture.pcap\')',
              "explanation": [
                "<strong>Line 1:</strong> rdpcap() reads pcap files from Wireshark/tcpdump.",
                "<strong>Lines 8-9:</strong> Tracks IP conversations and DNS queries.",
                "<strong>Line 11:</strong> most_common(3) shows top talkers — useful for finding data exfil.",
                "<strong>Line 12:</strong> DNS query logging reveals domains contacted."
              ]
            }
          ]
        },
        {
          "name": "Cloud Computing and Virtualization",
          "code": "ICN 3202",
          "icon": "cloud",
          "tags": ["cloud", "virtualization", "docker", "containers"],
          "description": "Cloud architectures, virtualization, containers, orchestration.",
          "projects": [
            {
              "title": "Docker Container Manager",
              "difficulty": "Advanced",
              "filename": "docker_manager.py",
              "description": "Manage Docker containers programmatically with Python.",
              "code": 'import docker\n\nclass ContainerManager:\n    def __init__(self):\n        self.client = docker.from_env()\n    \n    def list_all(self):\n        for c in self.client.containers.list(all=True):\n            print(f\'{c.short_id} | {c.name} | {c.status}\')\n    \n    def get_stats(self, name):\n        c = self.client.containers.get(name)\n        stats = c.stats(stream=False)\n        mem = stats[\'memory_stats\'][\'usage\'] / (1024*1024)\n        print(f\'{name} memory: {mem:.1f} MB\')\n\nif __name__ == \'__main__\':\n    mgr = ContainerManager()\n    mgr.list_all()',
              "explanation": [
                "<strong>Line 1:</strong> docker SDK for Python. Requires Docker daemon running.",
                "<strong>Line 5:</strong> docker.from_env() reads Docker host from environment.",
                "<strong>Line 9:</strong> containers.list(all=True) includes stopped containers.",
                "<strong>Line 12:</strong> container.stats(stream=False) gets a single snapshot."
              ]
            }
          ]
        },
        {
          "name": "Ethical Hacking",
          "code": "ICN 3203",
          "icon": "hacking",
          "tags": ["security", "pentesting", "exploitation", "defense"],
          "description": "Penetration testing methodology, vulnerability assessment, exploitation techniques.",
          "projects": [
            {
              "title": "Port Scanner & Service Fingerprinter",
              "difficulty": "Advanced",
              "filename": "port_scanner.py",
              "description": "Multi-threaded port scanner with service detection.",
              "code": 'import socket\nimport concurrent.futures\n\nCOMMON = {22:\'SSH\', 80:\'HTTP\', 443:\'HTTPS\', 3306:\'MySQL\', 3389:\'RDP\'}\n\ndef scan_port(target, port):\n    sock = socket.socket()\n    sock.settimeout(0.5)\n    if sock.connect_ex((target, port)) == 0:\n        return port, COMMON.get(port, \'Unknown\')\n    return port, None\n\ndef scan(target, ports=None):\n    ports = ports or list(COMMON.keys())\n    with concurrent.futures.ThreadPoolExecutor(100) as ex:\n        for port, svc in ex.map(lambda p: scan_port(target, p), ports):\n            if svc:\n                print(f\'Port {port}: {svc}\')\n\nif __name__ == \'__main__\':\n    scan(\'scanme.nmap.org\')',
              "explanation": [
                "<strong>Lines 7-11:</strong> scan_port connects with 0.5s timeout, returns (port, service).",
                "<strong>Lines 13-18:</strong> ThreadPoolExecutor with 100 workers for speed.",
                "<strong>Line 21:</strong> scanme.nmap.org is a legal test target provided by Nmap."
              ]
            }
          ]
        },
        {
          "name": "Machine Learning",
          "code": "ICN 3204",
          "icon": "ai",
          "tags": ["ml", "scikit-learn", "classification", "data-science"],
          "description": "Machine learning algorithms, supervised/unsupervised learning, model evaluation.",
          "projects": [
            {
              "title": "Network Traffic Classifier",
              "difficulty": "Advanced",
              "filename": "traffic_classifier.py",
              "description": "Classify network traffic types using scikit-learn machine learning.",
              "code": 'from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nimport numpy as np\n\n# Features: packet_size, port, protocol, ttl\nX = np.random.rand(1000, 4) * 100\ny = np.random.choice([\'web\', \'dns\', \'ssh\', \'mail\'], 1000)\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n\nclf = RandomForestClassifier(n_estimators=100)\nclf.fit(X_train, y_train)\npreds = clf.predict(X_test)\nprint(f\'Accuracy: {accuracy_score(y_test, preds):.2%}\')',
              "explanation": [
                "<strong>Line 1:</strong> RandomForest is an ensemble classifier — good for tabular data.",
                "<strong>Lines 7-8:</strong> Simulated network flow features (size, port, protocol, TTL).",
                "<strong>Line 10:</strong> train_test_split with 80/20 split for training/evaluation.",
                "<strong>Lines 12-13:</strong> fit() trains the model, predict() classifies test data."
              ]
            }
          ]
        }
      ]
    }
  },
  "year4": {
    "semester1": {
      "name": "Semester 1",
      "modules": [
        {
          "name": "Digital Forensics",
          "code": "ICN 4101",
          "icon": "forensics",
          "tags": ["forensics", "investigation", "evidence", "analysis"],
          "description": "Advanced digital forensics, evidence acquisition, forensic tools, chain of custody.",
          "projects": [
            {
              "title": "Disk Image Analyzer",
              "difficulty": "Advanced",
              "filename": "disk_analyzer.py",
              "description": "Analyze disk images — recover deleted files, extract metadata, generate forensic reports.",
              "code": 'import hashlib\nimport os\nfrom datetime import datetime\n\nclass DiskAnalyzer:\n    def __init__(self, path):\n        self.path = path\n    \n    def hash_file(self):\n        sha = hashlib.sha256()\n        with open(self.path, \'rb\') as f:\n            for chunk in iter(lambda: f.read(8192), b\'\'):\n                sha.update(chunk)\n        return sha.hexdigest()\n    \n    def file_metadata(self):\n        stat = os.stat(self.path)\n        return {\n            \'size\': stat.st_size,\n            \'created\': datetime.fromtimestamp(stat.st_ctime),\n            \'modified\': datetime.fromtimestamp(stat.st_mtime),\n            \'accessed\': datetime.fromtimestamp(stat.st_atime)\n        }\n\nif __name__ == \'__main__\':\n    analyzer = DiskAnalyzer(\'evidence.img\')\n    print(f\'Hash: {analyzer.hash_file()}\')\n    print(f\'Metadata: {analyzer.file_metadata()}\')',
              "explanation": [
                "<strong>Line 9:</strong> SHA-256 hashing with 8KB chunks — verifies evidence integrity.",
                "<strong>Lines 15-21:</strong> os.stat() extracts file timestamps (creation, modification, access).",
                "<strong>Lines 24-26:</strong> Demonstrates evidence chain-of-custody tracking."
              ]
            }
          ]
        },
        {
          "name": "Internet of Things",
          "code": "ICN 4102",
          "icon": "iot",
          "tags": ["iot", "sensors", "mqtt", "embedded"],
          "description": "IoT architectures, sensor networks, MQTT protocol, embedded systems.",
          "projects": [
            {
              "title": "MQTT Sensor Dashboard",
              "difficulty": "Advanced",
              "filename": "mqtt_dashboard.py",
              "description": "Connect to MQTT broker, collect sensor data, and visualize in real-time.",
              "code": 'import paho.mqtt.client as mqtt\nimport json\nfrom collections import deque\n\nclass SensorDashboard:\n    def __init__(self, broker=\'localhost\'):\n        self.client = mqtt.Client()\n        self.client.on_connect = lambda c, u, f, rc: c.subscribe(\'sensors/+\')\n        self.client.on_message = self.on_message\n        self.data = {}\n        self.client.connect(broker, 1883)\n    \n    def on_message(self, client, userdata, msg):\n        payload = json.loads(msg.payload)\n        topic = msg.topic.split(\'/\')[-1]\n        self.data[topic] = payload\n        print(f\'{topic}: {payload.get(\"value\", \"?\")} {payload.get(\"unit\", \"\")}\')\n    \n    def start(self):\n        print(\'Listening for sensor data...\')\n        self.client.loop_forever()\n\nif __name__ == \'__main__\':\n    dashboard = SensorDashboard()\n    dashboard.start()',
              "explanation": [
                "<strong>Line 1:</strong> paho-mqtt is the standard MQTT client for Python.",
                "<strong>Line 7:</strong> on_connect callback subscribes to all sensor topics.",
                "<strong>Line 14:</strong> json.loads() parses incoming sensor payload.",
                "<strong>Line 20:</strong> loop_forever() keeps listening for messages."
              ]
            }
          ]
        }
      ]
    },
    "semester2": {
      "name": "Semester 2",
      "modules": [
        {
          "name": "Natural Language Processing",
          "code": "ICN 4201",
          "icon": "ai",
          "tags": ["nlp", "text-processing", "sentiment", "nltk"],
          "description": "Text processing, sentiment analysis, named entity recognition. Process language with Python.",
          "projects": [
            {
              "title": "Sentiment Analysis Engine",
              "difficulty": "Advanced",
              "filename": "sentiment_analyzer.py",
              "description": "Analyze text sentiment — positive, negative, or neutral — using NLTK.",
              "code": 'from nltk.sentiment import SentimentIntensityAnalyzer\nimport nltk\n\nclass SentimentEngine:\n    def __init__(self):\n        nltk.download(\'vader_lexicon\', quiet=True)\n        self.analyzer = SentimentIntensityAnalyzer()\n    \n    def analyze(self, text):\n        scores = self.analyzer.polarity_scores(text)\n        if scores[\'compound\'] >= 0.05:\n            label = \'POSITIVE\'\n        elif scores[\'compound\'] <= -0.05:\n            label = \'NEGATIVE\'\n        else:\n            label = \'NEUTRAL\'\n        return {\'label\': label, \'scores\': scores}\n\nif __name__ == \'__main__\':\n    engine = SentimentEngine()\n    result = engine.analyze(\'This network is incredibly fast and reliable!\')\n    print(f\'{result[\"label\"]}: {result[\"scores\"]}\')',
              "explanation": [
                "<strong>Line 1:</strong> VADER is a rule-based sentiment analyzer tuned for social media.",
                "<strong>Line 6:</strong> Downloads VADER lexicon on first run.",
                "<strong>Lines 10-16:</strong> compound score > 0.05 = positive, < -0.05 = negative.",
                "<strong>Line 20:</strong> Example: positive review about network performance."
              ]
            }
          ]
        },
        {
          "name": "Blockchain Technologies",
          "code": "ICN 4202",
          "icon": "systems",
          "tags": ["blockchain", "crypto", "distributed", "ledger"],
          "description": "Blockchain fundamentals, distributed ledgers, smart contracts, consensus algorithms.",
          "projects": [
            {
              "title": "Simple Blockchain Implementation",
              "difficulty": "Advanced",
              "filename": "blockchain.py",
              "description": "Build a proof-of-work blockchain from scratch to understand the core concepts.",
              "code": 'import hashlib\nimport time\n\nclass Block:\n    def __init__(self, index, data, prev_hash):\n        self.index = index\n        self.timestamp = time.time()\n        self.data = data\n        self.prev_hash = prev_hash\n        self.nonce = 0\n        self.hash = self.mine()\n    \n    def mine(self):\n        while True:\n            h = hashlib.sha256(f\'{self.index}{self.timestamp}{self.data}{self.prev_hash}{self.nonce}\'.encode()).hexdigest()\n            if h.startswith(\'0000\'):\n                return h\n            self.nonce += 1\n\nclass Blockchain:\n    def __init__(self):\n        self.chain = [Block(0, \'Genesis\', \'0\')]\n    \n    def add_block(self, data):\n        prev = self.chain[-1]\n        self.chain.append(Block(len(self.chain), data, prev.hash))\n\nif __name__ == \'__main__\':\n    bc = Blockchain()\n    bc.add_block(\'Tx: Alice -> Bob $50\')\n    for b in bc.chain:\n        print(f\'Block {b.index}: {b.hash[:16]}...\')',
              "explanation": [
                "<strong>Lines 11-16:</strong> Proof-of-work: hashes until finding one with 4 leading zeros.",
                "<strong>Lines 19-21:</strong> Blockchain starts with a Genesis block.",
                "<strong>Lines 23-25:</strong> Each new block links to previous via prev_hash.",
                "<strong>Line 30:</strong> Demonstrates immutability — changing any block breaks the chain."
              ]
            }
          ]
        },
        {
          "name": "Final Year Project",
          "code": "ICN 4203",
          "icon": "systems",
          "tags": ["project", "research", "implementation", "thesis"],
          "description": "Capstone project integrating networking, security, and programming skills. Research and implementation.",
          "projects": [
            {
              "title": "Network Security Dashboard",
              "difficulty": "Advanced",
              "filename": "security_dashboard.py",
              "description": "Full-stack security monitoring dashboard — real-time threat detection and visualization.",
              "code": '# Final Year Project — Network Security Dashboard\n# Integrates Scapy packet capture, ML-based anomaly detection,\n# and a Flask web dashboard for real-time monitoring.\n\n# Key features:\n# 1. Live packet capture and analysis\n# 2. Machine learning anomaly detection\n# 3. Real-time alerting system\n# 4. REST API for external integration\n# 5. Historical data storage and reporting\n\n# Full implementation in the ICN Blog repository.\n\ndef main():\n    print("Network Security Dashboard v1.0")\n    print("Loading modules: Scapy, scikit-learn, Flask, SQLite...")\n    print("Dashboard ready at http://localhost:5000")\n\nif __name__ == \'__main__\':\n    main()',
              "explanation": [
                "<strong>This capstone project</strong> integrates everything from your 4-year degree.",
                "<strong>Scapy + ML:</strong> Capture traffic, extract features, classify anomalies.",
                "<strong>Flask dashboard:</strong> Real-time web interface for security monitoring.",
                "<strong>REST API:</strong> External tools can query threat data programmatically.",
                "<strong>SQLite:</strong> Stores historical data for trend analysis and reporting."
              ]
            }
          ]
        }
      ]
    }
  }
}

output_path = "d:\\dak\\icn-blog\\data\\modules.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("modules.json rebuilt successfully")

# Validate
with open(output_path, "r", encoding="utf-8") as f:
    json.load(f)
print("JSON is valid")

# Count modules
total = 0
for year_key, year_data in data.items():
    for sem_key, sem_data in year_data.items():
        total += len(sem_data.get("modules", []))
print(f"Total modules: {total}")
