"""Patch portfolio identity text to align with ICN Blog."""
path = "d:\\dak\\icn-blog\\portfolio\\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix hero badge + title + description
old_hero = '''<span class="hero-badge">Senior Frontend Developer</span>
                <h1 class="hero-title">Crafting Digital <br>Experiences</h1>
                <p class="hero-desc">I design and develop responsive, user-friendly websites and applications with modern technologies and best practices. Focused on creating seamless user experiences with cutting-edge frontend technologies.</p>
                <p class="hero-meta">Open-source projects updated directly from GitHub — every new repo appears automatically here.</p>'''

new_hero = '''<span class="hero-badge">ICN Student & Python Developer</span>
                <h1 class="hero-title">Building Networks<br>with Code</h1>
                <p class="hero-desc">BSc Information & Computer Networking student turning classroom theory into practical tools. Python, networking, security, and automation — one project at a time.</p>
                <p class="hero-meta">Every repo here is a working project from my degree. Open-source and updated from GitHub automatically.</p>'''

if old_hero in content:
    content = content.replace(old_hero, new_hero)
    print("Fixed hero section")
else:
    print("Could not find hero text to replace")

# 2. Fix about section
old_about = '''<h3>Frontend Developer & UI Specialist</h3>
                    <p>With over 7 years of experience in frontend development, I specialize in creating responsive, performant web applications using modern JavaScript frameworks and libraries.</p>'''

new_about = '''<h3>Network Engineer & Python Developer</h3>
                    <p>BSc Information & Computer Networking student at MUST. I build practical Python tools that bridge networking theory with working code — network scanners, security analyzers, and automation scripts.</p>'''

if old_about in content:
    content = content.replace(old_about, new_about)
    print("Fixed about section")
else:
    print("Could not find about text to replace")

# 3. Fix the background degree text
old_degree = '<span>Bsc in Information and Computer Networking</span>'
new_degree = '<span>BSc Information & Computer Networking @ MUST</span>'
if old_degree in content:
    content = content.replace(old_degree, new_degree)
    print("Fixed degree text")

old_exp = '<span>3+ Years Experience</span>'
new_exp = '<span>Building since Year 1</span>'
if old_exp in content:
    content = content.replace(old_exp, new_exp)
    print("Fixed experience text")

# 4. Fix footer
old_footer_desc = '<p style="color: var(--text-secondary); margin-bottom: 20px;">Senior Frontend Developer specializing in creating exceptional digital experiences with modern web technologies.</p>'
new_footer_desc = '<p style="color: var(--text-secondary); margin-bottom: 20px;">ICN Student & Python Developer. Building networking and security tools from the ICN curriculum at MUST.</p>'
if old_footer_desc in content:
    content = content.replace(old_footer_desc, new_footer_desc)
    print("Fixed footer description")

# 5. Fix contact email
old_email = '<p>kisulodaud@gmail.com</p>'
new_email = '<p><a href="index.html">theOutcast @ ICN Blog</a></p>'
if old_email in content:
    content = content.replace(old_email, new_email)
    print("Fixed email")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Portfolio patched successfully")
