import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data_file = root / 'data' / 'modules.json'

with data_file.open('r', encoding='utf-8') as handle:
    data = json.load(handle)

projects = {
    'Programming Concepts': {
        'title': 'Semester Planner and Folder Organizer',
        'difficulty': 'Intermediate',
        'filename': 'semester_planner.py',
        'description': 'Create a semester planner that builds study folders and saves a JSON plan for your courses.',
        'code': """from pathlib import Path\nimport json\n\n\ndef build_course_plan(root):\n    root = Path(root)\n    root.mkdir(exist_ok=True)\n\n    structure = {\n        'Programming Concepts': ['notes', 'labs', 'assignments'],\n        'Networking Basics': ['notes', 'labs', 'packet-tracer'],\n        'Operating Systems': ['notes', 'scripts', 'reports'],\n    }\n\n    plan = {}\n    for course, folders in structure.items():\n        course_dir = root / course.lower().replace(' ', '-')\n        course_dir.mkdir(exist_ok=True)\n        for folder in folders:\n            (course_dir / folder).mkdir(exist_ok=True)\n        plan[course] = [str((course_dir / folder).relative_to(root)) for folder in folders]\n\n    (root / 'plan.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')\n    return plan\n\n\nif __name__ == '__main__':\n    plan = build_course_plan('semester-plan')\n    print('Created folders for', len(plan), 'courses.')\n""",
        'explanation': [
            'The task creates a folder structure for the semester using Python.',
            'It organizes course work into notes, labs, and assignments folders.',
            'The plan is saved as JSON so it can be reused later.'
        ],
    },
    'Computer Systems Architecture': {
        'title': 'System Hardware Profiler',
        'difficulty': 'Intermediate',
        'filename': 'system_profiler.py',
        'description': 'Collect CPU, memory, and disk information from the machine and print a hardware summary.',
        'code': """import platform\nimport psutil\n\n\ndef hardware_report():\n    mem = psutil.virtual_memory()\n    disk = psutil.disk_usage('/')\n    return {\n        'processor': platform.processor(),\n        'cpu_cores': psutil.cpu_count(logical=False),\n        'ram_gb': round(mem.total / (1024 ** 3), 2),\n        'disk_used_percent': disk.percent,\n    }\n\n\nif __name__ == '__main__':\n    print(hardware_report())\n""",
        'explanation': [
            'The script gathers system-level details using psutil.',
            'It reports the processor, core count, memory size, and disk usage.',
            'This is useful for hardware reviews and troubleshooting.'
        ],
    },
    'Computer Network Engineering': {
        'title': 'Network Host Discovery Tool',
        'difficulty': 'Intermediate',
        'filename': 'host_discovery.py',
        'description': 'Scan a local network range and list hosts that respond to a TCP port probe.',
        'code': """import ipaddress\nimport socket\n\n\ndef find_live_hosts(network, port=22, timeout=0.2):\n    net = ipaddress.ip_network(network, strict=False)\n    results = []\n    for ip in net.hosts():\n        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        sock.settimeout(timeout)\n        try:\n            sock.connect((str(ip), port))\n            results.append(str(ip))\n        except OSError:\n            pass\n        finally:\n            sock.close()\n    return results\n\n\nif __name__ == '__main__':\n    hosts = find_live_hosts('192.168.1.0/24')\n    print('Live hosts:', hosts)\n""",
        'explanation': [
            'The script iterates over a subnet and tries to connect to a specific TCP port.',
            'A successful connection indicates that the host is active.',
            'This is a practical first step in network discovery.'
        ],
    },
    'Operating Systems': {
        'title': 'Process Monitor',
        'difficulty': 'Intermediate',
        'filename': 'process_monitor.py',
        'description': 'Inspect running processes and report the highest-memory consumers on the system.',
        'code': """import psutil\n\n\ndef top_processes(limit=5):\n    processes = []\n    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):\n        try:\n            processes.append(proc.info)\n        except (psutil.NoSuchProcess, psutil.AccessDenied):\n            continue\n    processes.sort(key=lambda item: item.get('memory_percent', 0), reverse=True)\n    return processes[:limit]\n\n\nif __name__ == '__main__':\n    for proc in top_processes():\n        print(proc['pid'], proc['name'], f'CPU={proc[\"cpu_percent\"]}%', f'MEM={proc[\"memory_percent\"]}%')\n""",
        'explanation': [
            'The monitor uses psutil to inspect running processes.',
            'It helps identify resource-hungry tasks on the machine.',
            'This is a practical starting point for troubleshooting and system analysis.'
        ],
    },
    'Object Oriented Programming': {
        'title': 'Network Device Simulator',
        'difficulty': 'Intermediate',
        'filename': 'device_simulator.py',
        'description': 'Model routers and switches as classes with reusable methods and shared behavior.',
        'code': """class NetworkDevice:\n    def __init__(self, name, ip_address):\n        self.name = name\n        self.ip_address = ip_address\n        self.online = False\n\n    def ping(self):\n        self.online = True\n        return self.online\n\n\nclass Router(NetworkDevice):\n    def __init__(self, name, ip_address, model):\n        super().__init__(name, ip_address)\n        self.model = model\n        self.routes = []\n\n    def add_route(self, network, gateway):\n        self.routes.append((network, gateway))\n\n\nif __name__ == '__main__':\n    router = Router('Core-R1', '192.168.1.1', 'ISR 4331')\n    router.add_route('10.0.0.0/8', '192.168.1.254')\n    print(router.name, router.model, router.routes)\n""",
        'explanation': [
            'The project uses inheritance to represent different network hardware types.',
            'A base class handles common behavior such as online state and pinging.',
            'Child classes add hardware-specific features like routing tables.'
        ],
    },
    'Data Communication': {
        'title': 'Packet Frame Decoder',
        'difficulty': 'Intermediate',
        'filename': 'frame_decoder.py',
        'description': 'Decode a simple binary frame into readable fields for a protocol simulator.',
        'code': """import struct\n\n\ndef decode_frame(frame):\n    header = struct.unpack('!HHB', frame[:7])\n    return {\n        'source': header[0],\n        'destination': header[1],\n        'type': header[2],\n        'payload': frame[7:].decode('utf-8', errors='ignore'),\n    }\n\n\nif __name__ == '__main__':\n    sample = b'\\x00\\x01\\x00\\x02\\x03hello'\n    print(decode_frame(sample))\n""",
        'explanation': [
            'The example shows how a network frame can be unpacked into meaningful fields.',
            'Struct is used to read header values from a byte stream.',
            'This is a strong foundation for understanding low-level communication.'
        ],
    },
    'Routing and Switching': {
        'title': 'Static Route Simulator',
        'difficulty': 'Intermediate',
        'filename': 'route_simulator.py',
        'description': 'Model static routes and choose the best path by matching the longest prefix.',
        'code': """from ipaddress import ip_network, ip_address\n\n\ndef best_route(destination, routes):\n    dest = ip_address(destination)\n    best = None\n    best_prefix = -1\n\n    for network, gateway in routes:\n        net = ip_network(network)\n        if dest in net:\n            prefix = net.prefixlen\n            if prefix > best_prefix:\n                best = gateway\n                best_prefix = prefix\n\n    return best\n\n\nif __name__ == '__main__':\n    routes = [('10.0.0.0/8', '192.168.1.254'), ('10.1.0.0/16', '192.168.2.1')]\n    print(best_route('10.1.5.8', routes))\n""",
        'explanation': [
            'The script stores multiple routes and tests which one matches the destination best.',
            'The longest-prefix rule is used to pick the most specific route.',
            'This mirrors how routing tables choose the best path.'
        ],
    },
    'Database Design and Implementation': {
        'title': 'Inventory Database Manager',
        'difficulty': 'Intermediate',
        'filename': 'inventory_db.py',
        'description': 'Create a SQLite database for tracking devices and support create-read-update-delete actions.',
        'code': """import sqlite3\n\n\nclass InventoryDB:\n    def __init__(self, db_name='inventory.db'):\n        self.conn = sqlite3.connect(db_name)\n        self.conn.execute('''\n            CREATE TABLE IF NOT EXISTS devices (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                name TEXT NOT NULL,\n                ip TEXT UNIQUE NOT NULL,\n                type TEXT NOT NULL\n            )\n        ''')\n        self.conn.commit()\n\n    def add_device(self, name, ip, device_type):\n        self.conn.execute(\n            'INSERT INTO devices (name, ip, type) VALUES (?, ?, ?)',\n            (name, ip, device_type),\n        )\n        self.conn.commit()\n\n    def list_devices(self):\n        return self.conn.execute('SELECT id, name, ip, type FROM devices ORDER BY name').fetchall()\n\n\nif __name__ == '__main__':\n    db = InventoryDB()\n    db.add_device('Core-SW1', '10.0.0.1', 'Switch')\n    print(db.list_devices())\n""",
        'explanation': [
            'The project creates a real SQLite database with a devices table.',
            'It supports adding devices and reading them back from storage.',
            'This is a practical database project for a networking lab.'
        ],
    },
    'Hardware and Software Integration': {
        'title': 'Serial Device Connector',
        'difficulty': 'Intermediate',
        'filename': 'serial_connector.py',
        'description': 'Open a serial connection to a device, read data, and print the result in a clean format.',
        'code': """import sys\ntry:\n    import serial\nexcept ImportError:\n    print('Install pyserial to run this example.')\n    sys.exit(0)\n\n\ndef read_from_port(port, baud_rate=9600):\n    with serial.Serial(port, baud_rate, timeout=1) as device:\n        device.write(b'AT\\n')\n        return device.readline().decode('utf-8', errors='ignore').strip()\n\n\nif __name__ == '__main__':\n    print(read_from_port('COM3'))\n""",
        'explanation': [
            'The project demonstrates how software can communicate with hardware over a serial port.',
            'It sends a simple command and reads the response from the device.',
            'This is a realistic workflow used in embedded and lab environments.'
        ],
    },
    'Computer Network Management': {
        'title': 'Switch Port Inventory Manager',
        'difficulty': 'Intermediate',
        'filename': 'switch_inventory.py',
        'description': 'Record switch ports, their VLANs, and their current state in a small management tool.',
        'code': """from collections import defaultdict\n\n\ndef build_port_report(ports):\n    report = defaultdict(list)\n    for port in ports:\n        report[port['vlan']].append(port['name'])\n    return dict(report)\n\n\nif __name__ == '__main__':\n    ports = [\n        {'name': 'Gi0/1', 'vlan': 10, 'state': 'up'},\n        {'name': 'Gi0/2', 'vlan': 10, 'state': 'up'},\n        {'name': 'Gi0/3', 'vlan': 20, 'state': 'down'},\n    ]\n    print(build_port_report(ports))\n""",
        'explanation': [
            'The script groups switch ports by VLAN so they can be reviewed as a report.',
            'It shows how an inventory tool can help keep track of distributed network devices.',
            'This is useful in network operations and troubleshooting.'
        ],
    },
    'Information Systems': {
        'title': 'Department Operations Reporter',
        'difficulty': 'Intermediate',
        'filename': 'operations_report.py',
        'description': 'Summarize department workloads and export a simple operations report.',
        'code': """import csv\n\n\ndef write_report(records, output_path):\n    fields = ['department', 'tasks', 'completed']\n    with open(output_path, 'w', newline='', encoding='utf-8') as handle:\n        writer = csv.DictWriter(handle, fieldnames=fields)\n        writer.writeheader()\n        writer.writerows(records)\n\n\nif __name__ == '__main__':\n    records = [\n        {'department': 'IT', 'tasks': 15, 'completed': 12},\n        {'department': 'Admin', 'tasks': 9, 'completed': 8},\n    ]\n    write_report(records, 'operations.csv')\n    print('Report saved to operations.csv')\n""",
        'explanation': [
            'The program writes a CSV report from department operation data.',
            'It formats records in a way that is useful for daily reporting or management reviews.',
            'This reflects how information systems support decision-making.'
        ],
    },
    'Linear Algebra and Calculus': {
        'title': 'Vector and Matrix Playground',
        'difficulty': 'Intermediate',
        'filename': 'vector_matrix.py',
        'description': 'Perform vector addition and matrix multiplication with a simple numerical toolkit.',
        'code': """import numpy as np\n\n\ndef add_vectors(a, b):\n    return (np.array(a) + np.array(b)).tolist()\n\n\ndef multiply_matrices(a, b):\n    return (np.array(a) @ np.array(b)).tolist()\n\n\nif __name__ == '__main__':\n    print(add_vectors([1, 2, 3], [4, 5, 6]))\n    print(multiply_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]))\n""",
        'explanation': [
            'The project uses NumPy to carry out basic linear algebra operations.',
            'Vector addition and matrix multiplication are core mathematical tasks used in many applications.',
            'This is a strong bridge between mathematics and programming.'
        ],
    },
    'Linux Operating System': {
        'title': 'System Health Reporter',
        'difficulty': 'Intermediate',
        'filename': 'system_health.py',
        'description': 'Collect key Linux system details such as uptime, memory, and disk usage into one living report.',
        'code': """import os\nimport shutil\n\n\ndef health_summary():\n    with open('/proc/uptime', 'r', encoding='utf-8') as handle:\n        uptime = float(handle.read().split()[0])\n    mem = shutil.disk_usage('/')\n    return {\n        'uptime_seconds': int(uptime),\n        'disk_total_gb': round(mem.total / (1024 ** 3), 2),\n        'disk_used_gb': round(mem.used / (1024 ** 3), 2),\n    }\n\n\nif __name__ == '__main__':\n    print(health_summary())\n""",
        'explanation': [
            'The script reads Linux system information from the /proc filesystem and disk utilities.',
            'It produces a compact report that can be used for monitoring or administration.',
            'This shows how operating systems expose useful information to tools and scripts.'
        ],
    },
    'Artificial Intelligence': {
        'title': 'Rule-Based Spam Classifier',
        'difficulty': 'Intermediate',
        'filename': 'spam_classifier.py',
        'description': 'Build a lightweight text classifier that uses keyword rules to label messages.',
        'code': """def classify_message(text):\n    lowered = text.lower()\n    spam_keywords = ['buy', 'win', 'click', 'offer', 'free']\n    score = sum(1 for keyword in spam_keywords if keyword in lowered)\n    return 'spam' if score >= 2 else 'safe'\n\n\nif __name__ == '__main__':\n    samples = ['Win a free tablet now', 'Project update for today']\n    for sample in samples:\n        print(sample, '=>', classify_message(sample))\n""",
        'explanation': [
            'The program uses a simple rule-based approach to classify text.',
            'Keyword matching is one of the earliest and most understandable forms of AI.',
            'It demonstrates how a small model can make decisions from text input.'
        ],
    },
    'Enterprise Wireless Design': {
        'title': 'Coverage Planner',
        'difficulty': 'Intermediate',
        'filename': 'coverage_planner.py',
        'description': 'Estimate indoor wireless coverage using a simple signal-strength model.',
        'code': """def estimate_signal(tx_power, distance, wall_penalty=5):\n    signal = tx_power - (distance * 3) - wall_penalty\n    return round(signal, 2)\n\n\nif __name__ == '__main__':\n    print(estimate_signal(20, 4, 6))\n""",
        'explanation': [
            'The script estimates received signal strength with a basic path-loss model.',
            'It shows how distance and walls reduce wireless quality in a simple way.',
            'This is a practical introduction to wireless planning.'
        ],
    },
    'Networking Troubleshooting': {
        'title': 'Connectivity Diagnostic Tool',
        'difficulty': 'Intermediate',
        'filename': 'connectivity_diagnostics.py',
        'description': 'Test DNS resolution and TCP connectivity for a host to diagnose common connectivity issues.',
        'code': """import socket\n\n\ndef diagnose(host):\n    results = {'dns': None, 'tcp': None}\n    try:\n        results['dns'] = socket.gethostbyname(host)\n    except socket.gaierror:\n        results['dns'] = 'UNRESOLVED'\n\n    try:\n        with socket.create_connection((host, 80), timeout=2):\n            results['tcp'] = 'OPEN'\n    except OSError:\n        results['tcp'] = 'CLOSED'\n\n    return results\n\n\nif __name__ == '__main__':\n    print(diagnose('example.com'))\n""",
        'explanation': [
            'The tool checks whether a host can be resolved and whether it accepts a TCP connection.',
            'This mirrors the basic steps used during real network troubleshooting.',
            'The script is valuable for isolating DNS or reachability problems.'
        ],
    },
    'Web Technologies': {
        'title': 'Static Page Analyzer',
        'difficulty': 'Intermediate',
        'filename': 'page_analyzer.py',
        'description': 'Parse a simple HTML page and count headings, paragraphs, and links.',
        'code': """from html.parser import HTMLParser\n\n\nclass PageParser(HTMLParser):\n    def __init__(self):\n        super().__init__()\n        self.counts = {'h1': 0, 'p': 0, 'a': 0}\n\n    def handle_starttag(self, tag, attrs):\n        if tag in self.counts:\n            self.counts[tag] += 1\n\n\nif __name__ == '__main__':\n    html = '<h1>Welcome</h1><p>Hello</p><a href=\"#\">Link</a>'\n    parser = PageParser()\n    parser.feed(html)\n    print(parser.counts)\n""",
        'explanation': [
            'The parser inspects a block of HTML and counts key elements.',
            'This shows how web pages can be analyzed programmatically.',
            'It is useful for understanding page structure or validating content.'
        ],
    },
    'Network Security': {
        'title': 'Password and Access Review Tool',
        'difficulty': 'Intermediate',
        'filename': 'access_review.py',
        'description': 'Validate password strength and analyze a simple access log for suspicious activity.',
        'code': """import re\n\n\ndef password_strength(password):\n    if len(password) >= 12 and re.search(r'\\d', password) and re.search(r'[A-Z]', password):\n        return 'strong'\n    return 'weak'\n\n\ndef flag_suspicious(logs):\n    suspicious = []\n    for entry in logs:\n        if 'FAIL' in entry.upper() and '3' in entry:\n            suspicious.append(entry)\n    return suspicious\n\n\nif __name__ == '__main__':\n    print(password_strength('SecurePass2026'))\n    print(flag_suspicious(['FAIL login 1', 'FAIL login 2', 'OK login 1']))\n""",
        'explanation': [
            'The project combines password validation with a basic security log review.',
            'It demonstrates how security checks can be automated in a lightweight tool.',
            'This is a practical starting point for identity and access tasks.'
        ],
    },
    'Big Data': {
        'title': 'Sales Data Analyzer',
        'difficulty': 'Intermediate',
        'filename': 'sales_analyzer.py',
        'description': 'Load CSV data, summarize key metrics, and identify the top-selling products.',
        'code': """import csv\nfrom collections import defaultdict\n\n\ndef analyze_sales(csv_path):\n    totals = defaultdict(float)\n    with open(csv_path, newline='', encoding='utf-8') as handle:\n        reader = csv.DictReader(handle)\n        for row in reader:\n            totals[row['product']] += float(row['amount'])\n    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))\n\n\nif __name__ == '__main__':\n    print(analyze_sales('sales.csv'))\n""",
        'explanation': [
            'The project reads row-based data from a CSV file and aggregates it into totals.',
            'This is the kind of workflow used in analytics and reporting pipelines.',
            'It demonstrates how simple analysis can scale to larger datasets.'
        ],
    },
    'Network Forensics': {
        'title': 'Timeline Builder from Logs',
        'difficulty': 'Intermediate',
        'filename': 'timeline_builder.py',
        'description': 'Parse log lines and turn them into a chronological timeline for investigation.',
        'code': """import re\n\n\ndef build_timeline(lines):\n    timeline = []\n    pattern = re.compile(r'(\\d{2}:\\d{2})\\s+(.*)')\n    for line in lines:\n        match = pattern.match(line)\n        if match:\n            timeline.append((match.group(1), match.group(2)))\n    return sorted(timeline)\n\n\nif __name__ == '__main__':\n    sample = ['10:00 Login attempt', '10:05 Logout', '10:10 Failed login']\n    print(build_timeline(sample))\n""",
        'explanation': [
            'The script extracts timestamps from logs and sorts them into a timeline.',
            'A timeline is extremely useful in incident analysis and forensics.',
            'This shows how evidence can be organized into a narrative.'
        ],
    },
    'Cloud Computing and Virtualization': {
        'title': 'VM Sizing Planner',
        'difficulty': 'Intermediate',
        'filename': 'vm_planner.py',
        'description': 'Estimate the resources needed for a set of virtual machines and summarize them.',
        'code': """def plan_vms(requirements):\n    total_cpu = sum(item['cpu'] for item in requirements)\n    total_ram = sum(item['ram_gb'] for item in requirements)\n    return {'total_cpu': total_cpu, 'total_ram_gb': total_ram}\n\n\nif __name__ == '__main__':\n    workloads = [\n        {'name': 'web', 'cpu': 2, 'ram_gb': 4},\n        {'name': 'db', 'cpu': 4, 'ram_gb': 8},\n    ]\n    print(plan_vms(workloads))\n""",
        'explanation': [
            'The planner totals CPU and RAM requirements for a small virtual infrastructure.',
            'This is useful when estimating capacity for cloud deployments.',
            'It demonstrates the thinking behind resource planning in virtualization.'
        ],
    },
    'Ethical Hacking': {
        'title': 'Safe Port Scanner',
        'difficulty': 'Intermediate',
        'filename': 'safe_port_scanner.py',
        'description': 'Probe a host for commonly used TCP ports using a controlled and lightweight scan.',
        'code': """import socket\n\n\ndef scan_ports(host, ports):\n    found = []\n    for port in ports:\n        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:\n            sock.settimeout(0.2)\n            try:\n                sock.connect((host, port))\n                found.append(port)\n            except OSError:\n                pass\n    return found\n\n\nif __name__ == '__main__':\n    print(scan_ports('localhost', [22, 80, 443]))\n""",
        'explanation': [
            'The scanner checks whether selected ports are open on a host.',
            'It shows the basics of port enumeration in a safe and educational way.',
            'This is a foundation for authorized security testing.'
        ],
    },
    'Machine Learning': {
        'title': 'Nearest Neighbour Classifier',
        'difficulty': 'Intermediate',
        'filename': 'nearest_neighbour.py',
        'description': 'Classify sample points by comparing them to known examples using k-nearest neighbors.',
        'code': """from math import sqrt\n\n\ndef classify(point, examples, k=3):\n    distances = []\n    for values, label in examples:\n        dist = sqrt(sum((a - b) ** 2 for a, b in zip(point, values)))\n        distances.append((dist, label))\n\n    distances.sort(key=lambda item: item[0])\n    votes = [label for _, label in distances[:k]]\n    return max(set(votes), key=votes.count)\n\n\nif __name__ == '__main__':\n    examples = [([1, 1], 'A'), ([2, 2], 'B'), ([3, 3], 'B')]\n    print(classify([1.2, 1.1], examples))\n""",
        'explanation': [
            'The script uses distance-based classification to predict a label for a new point.',
            'This is one of the simplest machine learning approaches.',
            'It demonstrates how training examples can guide predictions.'
        ],
    },
    'Digital Forensics': {
        'title': 'Hash and File Review Tool',
        'difficulty': 'Intermediate',
        'filename': 'hash_review.py',
        'description': 'Generate hashes for files and identify suspicious content based on file extensions.',
        'code': """import hashlib\nfrom pathlib import Path\n\n\ndef hash_file(path):\n    digest = hashlib.sha256()\n    with open(path, 'rb') as handle:\n        for chunk in iter(lambda: handle.read(1024 * 1024), b''):\n            digest.update(chunk)\n    return digest.hexdigest()\n\n\nif __name__ == '__main__':\n    print(hash_file('sample.txt'))\n""",
        'explanation': [
            'The script creates a cryptographic hash for a file to help with integrity checks.',
            'Hashing is a core technique in digital forensics and evidence handling.',
            'It provides a simple way to verify whether files have changed.'
        ],
    },
    'Internet of Things': {
        'title': 'Sensor Data Logger',
        'difficulty': 'Intermediate',
        'filename': 'sensor_logger.py',
        'description': 'Capture readings from a simple sensor stream and raise alerts when thresholds are exceeded.',
        'code': """def alert_if_high(readings, threshold=30):\n    alerts = []\n    for reading in readings:\n        if reading['value'] > threshold:\n            alerts.append(reading)\n    return alerts\n\n\nif __name__ == '__main__':\n    sensors = [{'device': 'temp-1', 'value': 35}, {'device': 'temp-2', 'value': 22}]\n    print(alert_if_high(sensors))\n""",
        'explanation': [
            'The project logs sensor values and flags those above a threshold.',
            'This is a practical introduction to IoT monitoring and alerting.',
            'It shows how simple devices can feed into a decision loop.'
        ],
    },
    'Natural Language Processing': {
        'title': 'Keyword Extractor',
        'difficulty': 'Intermediate',
        'filename': 'keyword_extractor.py',
        'description': 'Extract the most meaningful words from a text document using simple frequency analysis.',
        'code': """import re\nfrom collections import Counter\n\n\ndef extract_keywords(text, limit=5):\n    words = re.findall(r'\\b[a-z]{3,}\\b', text.lower())\n    counter = Counter(words)\n    return [word for word, _ in counter.most_common(limit)]\n\n\nif __name__ == '__main__':\n    text = 'Python is useful for text mining and natural language processing tasks.'\n    print(extract_keywords(text))\n""",
        'explanation': [
            'The script tokenizes text and ranks words by frequency.',
            'This is a lightweight approach to NLP that is easy to understand and build on.',
            'It is a useful starting point for text analytics.'
        ],
    },
    'Blockchain Technologies': {
        'title': 'Simple Blockchain',
        'difficulty': 'Intermediate',
        'filename': 'simple_blockchain.py',
        'description': 'Create a minimal blockchain with hashes, blocks, and a basic chain validation step.',
        'code': """import hashlib\n\n\nclass Block:\n    def __init__(self, index, payload, previous_hash):\n        self.index = index\n        self.payload = payload\n        self.previous_hash = previous_hash\n        self.hash = self._hash_block()\n\n    def _hash_block(self):\n        text = f'{self.index}{self.payload}{self.previous_hash}'.encode()\n        return hashlib.sha256(text).hexdigest()\n\n\nif __name__ == '__main__':\n    first = Block(0, 'Genesis', '0')\n    second = Block(1, 'Hello', first.hash)\n    print(first.hash)\n    print(second.hash)\n""",
        'explanation': [
            'The project builds a tiny blockchain using cryptographic hashes.',
            'It demonstrates the basic mechanism behind chaining blocks together.',
            'This is a strong introduction to blockchain concepts without the complexity of a full network.'
        ],
    },
    'Final Year Project': {
        'title': 'Capstone Project Tracker',
        'difficulty': 'Advanced',
        'filename': 'capstone_tracker.py',
        'description': 'Track project milestones, mark progress, and generate a simple progress report.',
        'code': """def progress_report(tasks):\n    report = []\n    for task in tasks:\n        percent = int(task['completed'] / task['total'] * 100)\n        report.append({'name': task['name'], 'progress': f'{percent}%'} )\n    return report\n\n\nif __name__ == '__main__':\n    tasks = [\n        {'name': 'Research', 'completed': 4, 'total': 5},\n        {'name': 'Implementation', 'completed': 6, 'total': 10},\n    ]\n    print(progress_report(tasks))\n""",
        'explanation': [
            'The script turns project milestones into a progress report.',
            'This is useful for capstone management and stakeholder updates.',
            'It shows how planning and tracking can be handled in a simple Python tool.'
        ],
    },
}

for year_key, year_data in data.items():
    for sem_key, sem_data in year_data.items():
        for module in sem_data.get('modules', []):
            name = module.get('name')
            if name in projects:
                module['projects'] = [projects[name]]

with data_file.open('w', encoding='utf-8') as handle:
    json.dump(data, handle, indent=2, ensure_ascii=False)
    handle.write('\n')

print(f'Updated {data_file}')
