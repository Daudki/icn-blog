#!/usr/bin/env python3
"""
ICN Blog — Static Site Builder
Reads data/modules.json and generates the complete site.
Run: python build.py
Output: build/ directory with complete static site
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime


class ICNBuilder:
    def __init__(self):
        self.root = Path(__file__).parent
        self.build_dir = self.root / 'build'
        self.data_file = self.root / 'data' / 'modules.json'
        self.components_dir = self.root / 'components'

        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.all_modules = self._flatten_modules()

    # ============================================
    # COMPONENTS
    # ============================================

    def _read_component(self, name):
        """Read a component HTML file."""
        path = self.components_dir / f'{name}.html'
        if path.exists():
            return path.read_text(encoding='utf-8').strip()
        return f'<!-- {name} component missing -->'

    def _footer(self):
        return self._read_component('footer')

    def _sidebar(self):
        return self._read_component('sidebar')

    # ============================================
    # FLATTEN MODULE DATA
    # ============================================

    def _flatten_modules(self):
        flat = []
        for year_key, year_data in self.data.items():
            year_num = int(year_key.replace('year', ''))
            for sem_key, sem_data in year_data.items():
                sem_num = int(sem_key.replace('semester', ''))
                for mod in sem_data.get('modules', []):
                    slug = self._slugify(mod['name'])
                    flat.append({
                        **mod,
                        'year_key': year_key,
                        'year_num': year_num,
                        'year_label': f'Year {year_num}',
                        'sem_key': sem_key,
                        'sem_num': sem_num,
                        'sem_label': sem_data.get('name', f'Semester {sem_num}'),
                        'slug': slug,
                        'url': f'modules/{year_key}/{slug}.html',
                        'project_count': len(mod.get('projects', []))
                    })
        return flat

    def _slugify(self, text):
        return text.lower().replace(' & ', '-').replace(' ', '-').replace('/', '-')

    # ============================================
    # BUILD
    # ============================================

    def build(self):
        print("\n🔨 Building ICN Blog...\n")

        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir()

        # Copy static assets
        for folder in ['css', 'js', 'images', 'assets']:
            src = self.root / folder
            if src.exists():
                shutil.copytree(src, self.build_dir / folder)
                print(f"📁 Copied {folder}/")

        # Copy data directory (for search to work)
        data_dst = self.build_dir / 'data'
        data_dst.mkdir(exist_ok=True)
        shutil.copy2(self.data_file, data_dst / 'modules.json')
        print(f"📁 Copied data/modules.json")

        # Copy portfolio
        portfolio_src = self.root / 'portfolio'
        if portfolio_src.exists():
            shutil.copytree(portfolio_src, self.build_dir / 'portfolio')
            print(f"📁 Copied portfolio/")

        # Copy root-level pages
        for page in ['about.html', 'search.html']:
            src = self.root / page
            if src.exists():
                shutil.copy2(src, self.build_dir / page)
                print(f"📄 Copied {page}")

        # Build index.html
        self._build_index()
        print(f"📄 Built: index.html")

        # Build all module pages
        self._build_module_pages()

        # Build sitemap
        self._build_sitemap()
        print(f"📄 Built: sitemap.xml")

        print(f"\n✅ Build complete! Output: {self.build_dir}")
        print(f"   Open {self.build_dir}/index.html to preview.")

    # ============================================
    # BUILD INDEX.HTML
    # ============================================

    def _build_index(self):
        total_modules = len(self.all_modules)
        total_projects = sum(m['project_count'] for m in self.all_modules)

        years = {}
        for m in self.all_modules:
            yk = m['year_key']
            if yk not in years:
                years[yk] = {'label': m['year_label'], 'num': m['year_num'], 'modules': []}
            years[yk]['modules'].append(m)

        year_card_info = {
            'year1': {'title': 'Foundation', 'desc': 'Programming, Networking Basics, OS, Architecture', 'color': 'y1'},
            'year2': {'title': 'Intermediate', 'desc': 'Network Mgmt, Linux, AI, Information Systems', 'color': 'y2'},
            'year3': {'title': 'Advanced', 'desc': 'Security, Forensics, Cloud, Ethical Hacking, ML', 'color': 'y3'},
            'year4': {'title': 'Specialization', 'desc': 'IoT, Digital Forensics, NLP, Blockchain, Final Project', 'color': 'y4'},
        }

        year_cards_html = ''
        for yk in ['year1', 'year2', 'year3', 'year4']:
            info = year_card_info[yk]
            count = len(years.get(yk, {}).get('modules', []))
            year_cards_html += f'''
                <div class="year-card {info['color']}" onclick="filterByYear('{yk}')">
                    <span class="badge">Year {yk[-1]}</span>
                    <h3>{info['title']}</h3>
                    <p>{info['desc']}</p>
                    <span class="count">{count} Modules</span>
                </div>'''

        modules_json = json.dumps([{
            'name': m['name'],
            'code': m.get('code', ''),
            'description': m.get('description', ''),
            'icon': m.get('icon', 'default'),
            'tags': m.get('tags', []),
            'year_key': m['year_key'],
            'year_label': m['year_label'],
            'sem_label': m['sem_label'],
            'slug': m['slug'],
            'url': m['url'],
            'project_count': m['project_count']
        } for m in self.all_modules])

        footer_html = self._footer()

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="ICN Blog — Python × Networking × Security. Practical projects for every module in the ICN degree at MUST.">
    <title>ICN Blog | Python × Networking × Security</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/responsive.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">
    <style>
        :root {{
            --bg: #0a0e17; --bg-card: #111827; --bg-hover: #1a2332; --border: #21262d;
            --text: #e6edf3; --text-muted: #8b949e; --accent: #58a6ff; --accent-hover: #79b8ff;
            --green: #3fb950; --orange: #d2991d; --red: #f85149; --purple: #a371f7;
            --radius: 8px; --max: 1200px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh;
        }}
        a {{ color: var(--accent); text-decoration: none; transition: color 0.15s; }}
        a:hover {{ color: var(--accent-hover); }}

        .header {{
            background: var(--bg-card); border-bottom: 1px solid var(--border);
            position: sticky; top: 0; z-index: 100;
        }}
        .header-inner {{
            max-width: var(--max); margin: 0 auto; padding: 0 1.25rem;
            display: flex; align-items: center; justify-content: space-between; height: 60px; gap: 1rem;
        }}
        .logo {{ display: flex; align-items: center; gap: 0.5rem; color: var(--text); font-weight: 700; font-size: 1.1rem; }}
        .logo i {{ color: var(--accent); font-size: 1.3rem; }}
        .nav {{ display: flex; gap: 0.25rem; }}
        .nav a {{
            color: var(--text-muted); padding: 0.4rem 0.75rem; border-radius: 6px; font-size: 0.85rem;
        }}
        .nav a:hover {{ color: var(--text); background: var(--bg-hover); }}
        .mobile-btn {{ display: none; background: none; border: none; color: var(--text); font-size: 1.3rem; cursor: pointer; }}

        .hero {{ text-align: center; padding: 3.5rem 1.25rem 2.5rem; max-width: 700px; margin: 0 auto; }}
        .hero-badge {{
            display: inline-block; background: rgba(88,166,255,0.1); color: var(--accent);
            padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
            margin-bottom: 1rem; border: 1px solid rgba(88,166,255,0.2);
        }}
        .hero h1 {{ font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 800; margin-bottom: 0.75rem; line-height: 1.2; }}
        .hero h1 span {{
            background: linear-gradient(135deg, var(--accent), var(--purple));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }}
        .hero p {{ color: var(--text-muted); font-size: 1.05rem; margin-bottom: 1.5rem; }}
        .hero-btns {{ display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; }}
        .btn {{
            display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.65rem 1.4rem;
            border-radius: var(--radius); font-weight: 600; font-size: 0.9rem; cursor: pointer;
            border: 1px solid transparent; transition: all 0.2s;
        }}
        .btn-primary {{ background: var(--accent); color: #000; }}
        .btn-primary:hover {{ background: var(--accent-hover); color: #000; }}
        .btn-outline {{ background: transparent; color: var(--text); border-color: var(--border); }}
        .btn-outline:hover {{ border-color: var(--accent); color: var(--accent); }}

        .stats {{
            max-width: var(--max); margin: 0 auto 2.5rem; padding: 0 1.25rem;
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
        }}
        .stat-card {{
            background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
            padding: 1.25rem; text-align: center;
        }}
        .stat-card i {{ font-size: 1.4rem; color: var(--accent); margin-bottom: 0.3rem; }}
        .stat-card .num {{ font-size: 1.8rem; font-weight: 800; display: block; }}
        .stat-card .lbl {{ color: var(--text-muted); font-size: 0.8rem; }}

        .section {{ max-width: var(--max); margin: 0 auto 3rem; padding: 0 1.25rem; }}
        .section h2 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 0.3rem; }}
        .section .sub {{ color: var(--text-muted); margin-bottom: 1.25rem; font-size: 0.95rem; }}

        .year-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }}
        .year-card {{
            background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
            padding: 1.5rem; cursor: pointer; transition: all 0.2s; position: relative;
        }}
        .year-card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
        .year-card .badge {{
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px;
            font-size: 0.7rem; font-weight: 700; margin-bottom: 0.75rem;
        }}
        .y1 .badge {{ background: rgba(63,185,80,0.15); color: var(--green); }}
        .y2 .badge {{ background: rgba(88,166,255,0.15); color: var(--accent); }}
        .y3 .badge {{ background: rgba(210,153,29,0.15); color: var(--orange); }}
        .y4 .badge {{ background: rgba(163,113,247,0.15); color: var(--purple); }}
        .year-card h3 {{ font-size: 1.05rem; margin-bottom: 0.3rem; }}
        .year-card p {{ color: var(--text-muted); font-size: 0.82rem; margin-bottom: 0.75rem; }}
        .year-card .count {{ font-size: 0.78rem; color: var(--accent); font-weight: 600; }}

        .controls {{ display: flex; gap: 0.75rem; margin-bottom: 1.25rem; flex-wrap: wrap; }}
        .search-box {{
            flex: 1; min-width: 200px; background: var(--bg-card); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 0.55rem 1rem; color: var(--text);
            font-size: 0.9rem; outline: none;
        }}
        .search-box:focus {{ border-color: var(--accent); }}
        .filter-row {{ display: flex; gap: 0.35rem; flex-wrap: wrap; }}
        .filter-btn {{
            background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted);
            padding: 0.4rem 0.8rem; border-radius: 20px; cursor: pointer; font-size: 0.78rem;
            transition: all 0.15s;
        }}
        .filter-btn:hover {{ color: var(--text); }}
        .filter-btn.active {{ background: var(--accent); color: #000; border-color: var(--accent); font-weight: 600; }}

        .module-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 0.85rem; }}
        .mod-card {{
            background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
            padding: 1.2rem; cursor: pointer; transition: all 0.2s; border-top: 3px solid var(--border);
        }}
        .mod-card:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }}
        .mod-card.y1 {{ border-top-color: var(--green); }}
        .mod-card.y2 {{ border-top-color: var(--accent); }}
        .mod-card.y3 {{ border-top-color: var(--orange); }}
        .mod-card.y4 {{ border-top-color: var(--purple); }}
        .mod-card .icon-row {{ display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem; }}
        .mod-card .icon-row i {{ font-size: 1.3rem; }}
        .mod-card .icon-row .code {{ font-size: 0.7rem; color: var(--accent); font-family: monospace; margin-left: auto; }}
        .mod-card h3 {{ font-size: 1rem; margin-bottom: 0.3rem; }}
        .mod-card .desc {{
            color: var(--text-muted); font-size: 0.82rem; margin-bottom: 0.75rem;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }}
        .mod-card .meta {{ display: flex; gap: 0.75rem; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem; }}
        .mod-card .meta i {{ margin-right: 0.2rem; }}
        .mod-card .bottom {{
            display: flex; justify-content: space-between; align-items: center;
            padding-top: 0.6rem; border-top: 1px solid var(--border); font-size: 0.78rem;
        }}
        .mod-card .bottom .projects {{ color: var(--green); }}
        .mod-card .bottom .arrow {{ color: var(--accent); opacity: 0; transition: opacity 0.2s; }}
        .mod-card:hover .bottom .arrow {{ opacity: 1; }}

        .no-results {{ grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted); }}
        .no-results i {{ font-size: 2.5rem; margin-bottom: 1rem; display: block; }}

        .tech-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 0.75rem; }}
        .tech-item {{
            background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
            padding: 1rem; text-align: center; transition: all 0.2s;
        }}
        .tech-item:hover {{ border-color: var(--accent); }}
        .tech-item i {{ font-size: 1.6rem; margin-bottom: 0.3rem; display: block; }}
        .tech-item span {{ font-size: 0.8rem; font-weight: 600; }}
        .tech-item small {{ display: block; color: var(--text-muted); font-size: 0.65rem; }}

        @media (max-width: 900px) {{ .year-grid {{ grid-template-columns: 1fr 1fr; }} }}
        @media (max-width: 768px) {{
            .nav {{ display: none; }}
            .nav.open {{
                display: flex; flex-direction: column; position: absolute; top: 60px; left: 0; right: 0;
                background: var(--bg-card); border-bottom: 1px solid var(--border); padding: 1rem;
            }}
            .mobile-btn {{ display: block; }}
            .stats {{ grid-template-columns: 1fr 1fr; }}
        }}
        @media (max-width: 500px) {{
            .year-grid {{ grid-template-columns: 1fr; }}
            .stats {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <a href="index.html" class="logo">
                <i class="fa-solid fa-network-wired"></i>
                ICN Blog
            </a>
            <nav class="nav" id="mainNav">
                <a href="index.html">Home</a>
                <a href="about.html">About</a>
                <a href="portfolio/index.html">Portfolio</a>
                <a href="search.html">Search</a>
                <a href="#modules">Modules</a>
            </nav>
            <button class="mobile-btn" id="mobileBtn" aria-label="Menu">
                <i class="fa-solid fa-bars"></i>
            </button>
        </div>
    </header>

    <main>
        <section class="hero">
            <span class="hero-badge">BSc Information & Computer Networking</span>
            <h1>From Theory to <span>Working Code</span></h1>
            <p>Every module in your degree transformed into practical Python projects. Understand networking, security, and automation by building real tools — with detailed, line-by-line explanations.</p>
            <div class="hero-btns">
                <a href="#modules" class="btn btn-primary"><i class="fa-solid fa-rocket"></i> Browse Modules</a>
                <a href="search.html" class="btn btn-outline"><i class="fa-solid fa-magnifying-glass"></i> Search</a>
            </div>
        </section>

        <section class="stats">
            <div class="stat-card"><i class="fa-solid fa-book"></i><span class="num">{total_modules}</span><span class="lbl">Python Modules</span></div>
            <div class="stat-card"><i class="fa-solid fa-diagram-project"></i><span class="num">{total_projects}</span><span class="lbl">Projects</span></div>
            <div class="stat-card"><i class="fa-solid fa-code"></i><span class="num">10K+</span><span class="lbl">Lines of Code</span></div>
            <div class="stat-card"><i class="fa-solid fa-graduation-cap"></i><span class="num">4</span><span class="lbl">Years</span></div>
        </section>

        <section class="section">
            <h2>Browse by Year</h2>
            <p class="sub">Content follows your university curriculum exactly</p>
            <div class="year-grid">{year_cards_html}
            </div>
        </section>

        <section class="section" id="modules">
            <h2>All Modules</h2>
            <p class="sub">Select a module to view projects and code</p>
            <div class="controls">
                <input type="text" class="search-box" id="searchInput" placeholder="Search modules... (e.g., python, security, networking)">
                <div class="filter-row" id="filterBtns">
                    <button class="filter-btn active" data-year="all">All Years</button>
                    <button class="filter-btn" data-year="year1">Year 1</button>
                    <button class="filter-btn" data-year="year2">Year 2</button>
                    <button class="filter-btn" data-year="year3">Year 3</button>
                    <button class="filter-btn" data-year="year4">Year 4</button>
                </div>
            </div>
            <div class="module-grid" id="moduleGrid"></div>
        </section>

        <section class="section">
            <h2>Technologies You'll Master</h2>
            <p class="sub">Build real tools with industry-standard Python libraries</p>
            <div class="tech-grid">
                <div class="tech-item"><i class="fa-brands fa-python" style="color:#3776AB;"></i><span>Python</span><small>Core language</small></div>
                <div class="tech-item"><i class="fa-solid fa-network-wired" style="color:#58a6ff;"></i><span>Scapy</span><small>Packet manipulation</small></div>
                <div class="tech-item"><i class="fa-solid fa-server" style="color:#d2991d;"></i><span>Netmiko</span><small>Network automation</small></div>
                <div class="tech-item"><i class="fa-solid fa-shield" style="color:#f85149;"></i><span>Cryptography</span><small>Encryption</small></div>
                <div class="tech-item"><i class="fa-solid fa-brain" style="color:#a371f7;"></i><span>Scikit-learn</span><small>Machine Learning</small></div>
                <div class="tech-item"><i class="fa-solid fa-globe" style="color:#14b8a6;"></i><span>Flask</span><small>Web dashboards</small></div>
                <div class="tech-item"><i class="fa-solid fa-cloud" style="color:#6366f1;"></i><span>Docker</span><small>Containerization</small></div>
                <div class="tech-item"><i class="fa-solid fa-database" style="color:#3fb950;"></i><span>SQLite</span><small>Data storage</small></div>
            </div>
        </section>
    </main>

    {footer_html}

    <script src="js/search.js"></script>
    <script src="js/utils.js"></script>
    <script>
        const ALL_MODULES = {modules_json};

        const ICONS = {{
            'programming': 'fa-code', 'networking': 'fa-network-wired', 'security': 'fa-shield-haltered',
            'data': 'fa-database', 'systems': 'fa-server', 'ai': 'fa-brain', 'web': 'fa-globe',
            'mobile': 'fa-mobile-screen', 'cloud': 'fa-cloud', 'iot': 'fa-microchip',
            'forensics': 'fa-magnifying-glass', 'hacking': 'fa-user-secret', 'default': 'fa-book'
        }};
        const COLORS = {{
            'programming': '#3fb950', 'networking': '#58a6ff', 'security': '#f85149',
            'data': '#d2991d', 'systems': '#a371f7', 'ai': '#ec4899', 'web': '#14b8a6',
            'default': '#8b949e'
        }};

        function getIcon(mod) {{ return ICONS[mod.icon] || ICONS['default']; }}
        function getColor(mod) {{ return COLORS[mod.icon] || COLORS['default']; }}
        function getYearClass(mod) {{
            return mod.year_key === 'year1' ? 'y1' : mod.year_key === 'year2' ? 'y2' :
                   mod.year_key === 'year3' ? 'y3' : 'y4';
        }}

        let currentFilter = 'all';
        let currentQuery = '';

        function renderModules() {{
            let filtered = ALL_MODULES;
            if (currentFilter !== 'all') filtered = filtered.filter(m => m.year_key === currentFilter);
            if (currentQuery.trim().length >= 2) {{
                const q = currentQuery.toLowerCase().trim();
                filtered = filtered.filter(m =>
                    m.name.toLowerCase().includes(q) ||
                    (m.code || '').toLowerCase().includes(q) ||
                    m.description.toLowerCase().includes(q) ||
                    m.tags.some(t => t.toLowerCase().includes(q))
                );
            }}

            const grid = document.getElementById('moduleGrid');
            if (filtered.length === 0) {{
                grid.innerHTML = '<div class="no-results"><i class="fa-solid fa-search"></i><h3>No modules found</h3><p>Try a different search term.</p></div>';
                return;
            }}

            grid.innerHTML = filtered.map(m => {{
                const color = getColor(m);
                return `<div class="mod-card ${{getYearClass(m)}}" onclick="window.location.href='${{m.url}}'" tabindex="0" onkeydown="if(event.key==='Enter')window.location.href='${{m.url}}'">
                    <div class="icon-row">
                        <i class="fa-solid ${{getIcon(m)}}" style="color:${{color}}"></i>
                        <span class="code">${{m.code || ''}}</span>
                    </div>
                    <h3>${{m.name}}</h3>
                    <p class="desc">${{m.description || ''}}</p>
                    <div class="meta">
                        <span><i class="fa-solid fa-calendar"></i> ${{m.year_label}}</span>
                        <span><i class="fa-solid fa-clock"></i> ${{m.sem_label}}</span>
                    </div>
                    <div class="bottom">
                        <span class="projects"><i class="fa-solid fa-code"></i> ${{m.project_count}} project${{m.project_count !== 1 ? 's' : ''}}</span>
                        <span class="arrow"><i class="fa-solid fa-arrow-right"></i></span>
                    </div>
                </div>`;
            }}).join('');
        }}

        function filterByYear(year) {{
            currentFilter = year;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            document.querySelector(`.filter-btn[data-year="${{year}}"]`)?.classList.add('active');
            renderModules();
            document.getElementById('modules').scrollIntoView({{ behavior: 'smooth' }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderModules();
            document.getElementById('footerYear').textContent = new Date().getFullYear();

            document.getElementById('searchInput').addEventListener('input', function() {{
                currentQuery = this.value;
                renderModules();
            }});

            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', () => filterByYear(btn.dataset.year));
            }});

            document.getElementById('mobileBtn').addEventListener('click', () => {{
                document.getElementById('mainNav').classList.toggle('open');
            }});
        }});
    </script>
</body>
</html>'''

        (self.build_dir / 'index.html').write_text(html, encoding='utf-8')

    # ============================================
    # BUILD MODULE PAGES
    # ============================================

    def _build_module_pages(self):
        for mod in self.all_modules:
            self._build_module_page(mod)
            print(f"📄 Built: {mod['url']}")

    def _build_module_page(self, mod):
        module_dir = self.build_dir / 'modules' / mod['year_key']
        module_dir.mkdir(parents=True, exist_ok=True)

        # Project sections
        projects_html = ''
        for i, proj in enumerate(mod.get('projects', [])):
            code_id = f"code-{i}"
            projects_html += f'''
                <div class="project-card">
                    <div class="project-header" onclick="this.parentElement.querySelector('.project-body').classList.toggle('open'); this.classList.toggle('open');">
                        <h3><i class="fa-solid fa-code"></i> {proj.get('title', 'Untitled Project')}</h3>
                        <span class="project-difficulty {proj.get('difficulty', 'Beginner')}">{proj.get('difficulty', 'Beginner')}</span>
                    </div>
                    <div class="project-body{' open' if i == 0 else ''}">
                        <p>{proj.get('description', '')}</p>
                        <div class="code-block">
                            <div class="code-header">
                                <span>{proj.get('filename', 'script.py')}</span>
                                <div>
                                    <button class="copy-btn" onclick="copyToClipboard(document.getElementById('{code_id}').textContent); this.classList.add('copied'); this.innerHTML='<i class=\\'fa-solid fa-check\\'></i> Copied!'; setTimeout(()=>{{this.classList.remove('copied'); this.innerHTML='<i class=\\'fa-solid fa-copy\\'></i> Copy';}},2000);"><i class="fa-solid fa-copy"></i> Copy</button>
                                    <button class="download-btn" data-filename="{proj.get('filename', 'script.py')}" data-code="{self._escape_attr(proj.get('code', ''))}" onclick="downloadFile(this.dataset.code, this.dataset.filename);"><i class="fa-solid fa-download"></i> Download</button>
                                </div>
                            </div>
                            <pre id="{code_id}"><code>{self._escape_html(proj.get('code', '# Code coming soon'))}</code></pre>
                        </div>
                        <div class="explanation">
                            <h4><i class="fa-solid fa-lightbulb"></i> Line-by-Line Explanation</h4>
                            <ol>
                                {''.join(f'<li>{exp}</li>' for exp in proj.get('explanation', ['No explanation yet.']))}
                            </ol>
                        </div>
                    </div>
                </div>'''

        first_project = mod.get('projects', [{}])[0]
        objectives_html = ''.join(
            f'<li><i class="fa-solid fa-check"></i> {obj}</li>'
            for obj in first_project.get('objectives', [
                f'Understand core concepts of {mod["name"]}',
                f'Apply {mod["name"]} concepts in Python',
                f'Build a working project from scratch'
            ])
        )

        footer_html = self._footer()
        sidebar_html = self._sidebar()

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{mod.get('description', '')}">
    <title>{mod['name']} — {mod.get('code', '')} | ICN Blog</title>
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" href="../../css/modules.css">
    <link rel="stylesheet" href="../../css/responsive.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="icon" href="../../assets/icons/favicon.svg" type="image/svg+xml">
</head>
<body>
    <header class="global-header">
        <div class="header-inner">
            <a href="../../index.html" class="header-logo">
                <i class="fa-solid fa-network-wired"></i>
                ICN Blog
            </a>
            <nav class="header-nav">
                <a href="../../index.html">Home</a>
                <a href="../../about.html">About</a>
                <a href="../../portfolio/index.html">Portfolio</a>
                <a href="../../search.html">Search</a>
                <a href="../../index.html#modules">Modules</a>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="breadcrumb-container">
            <ol>
                <li><a href="../../index.html"><i class="fa-solid fa-house"></i> Home</a></li>
                <li><a href="../../index.html#modules">Modules</a></li>
                <li><span aria-current="page">{mod['name']}</span></li>
            </ol>
        </div>
    </nav>

    <section class="module-hero">
        <div class="module-hero-container">
            <div class="module-hero-content">
                <span class="module-badge">{mod['year_label']} · {mod['sem_label']}</span>
                <h1>{mod['name']}</h1>
                <p class="module-code">{mod.get('code', '')}</p>
                <p class="module-description">{mod.get('description', '')}</p>
                <div class="module-meta">
                    <span><i class="fa-solid fa-code"></i> {mod['project_count']} Python Project{'s' if mod['project_count'] != 1 else ''}</span>
                    <span><i class="fa-solid fa-clock"></i> Self-paced</span>
                </div>
                <div class="module-tags">
                    {''.join(f'<span class="tag">{tag}</span>' for tag in mod.get('tags', []))}
                </div>
            </div>
            <div class="module-hero-visual">
                <div class="code-preview-window">
                    <div class="window-dots">
                        <span class="dot red"></span>
                        <span class="dot yellow"></span>
                        <span class="dot green"></span>
                    </div>
                    <pre><code># {mod.get('code', '')} — {mod['name']}
# {mod['year_label']} · {mod['sem_label']}
# {mod.get('project_count', 0)} Python project{'s' if mod.get('project_count', 0) != 1 else ''}</code></pre>
                </div>
            </div>
        </div>
    </section>

    <main class="module-layout">
        <div class="module-layout-container">
            {sidebar_html}

            <article class="module-article">
                <section class="module-section" id="overview">
                    <h2><i class="fa-solid fa-book-open"></i> Overview</h2>
                    <p>{mod.get('description', '')}</p>
                </section>

                <section class="module-section" id="objectives">
                    <h2><i class="fa-solid fa-list-check"></i> What You'll Learn</h2>
                    <ul class="objectives-list">{objectives_html}</ul>
                </section>

                <section class="module-section" id="projects">
                    <h2><i class="fa-solid fa-diagram-project"></i> Projects</h2>
                    {projects_html}
                </section>
            </article>
        </div>
    </main>

    <button class="back-to-top" id="backToTop" aria-label="Back to top">
        <i class="fa-solid fa-arrow-up"></i>
    </button>

    {footer_html}

    <script src="../../js/utils.js"></script>
    <script>
        document.getElementById('footerYear').textContent = new Date().getFullYear();

        const backToTop = document.getElementById('backToTop');
        window.addEventListener('scroll', () => {{
            backToTop.classList.toggle('visible', window.scrollY > 500);
        }});
        backToTop.addEventListener('click', () => {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function(e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>'''

        (module_dir / f"{mod['slug']}.html").write_text(html, encoding='utf-8')

    # ============================================
    # BUILD SITEMAP
    # ============================================

    def _build_sitemap(self):
        urls = ['index.html', 'about.html', 'search.html', 'portfolio/index.html']
        for m in self.all_modules:
            urls.append(m['url'])

        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in urls:
            sitemap += f'  <url><loc>https://icn-blog.com/{url}</loc><lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod></url>\n'
        sitemap += '</urlset>'
        (self.build_dir / 'sitemap.xml').write_text(sitemap, encoding='utf-8')

    # ============================================
    # HELPERS
    # ============================================

    def _escape_html(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def _escape_attr(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').replace('\n', '\\n')


if __name__ == '__main__':
    builder = ICNBuilder()
    builder.build()
