"""
templates/html_templates.py
All HTML page templates for File Organizer Pro.
Aesthetic: Dark industrial-glass with neon accents. Monospace + elegant serif pairing.
"""

# ── Shared base (nav + styles) ─────────────────────────────────────────────────
BASE_STYLE = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Playfair+Display:wght@600;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --card:      #161b22;
    --border:    #21262d;
    --neon:      #00ff88;
    --neon2:     #00cfff;
    --orange:    #ff6b35;
    --purple:    #bf5af2;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --radius:    10px;
    --font-mono: 'JetBrains Mono', monospace;
    --font-disp: 'Playfair Display', serif;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 14px;
    min-height: 100vh;
  }
  a { color: var(--neon); text-decoration: none; }
  a:hover { text-decoration: underline; }

  /* ── NAV ── */
  nav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,12,16,0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 56px;
  }
  .nav-brand {
    font-family: var(--font-disp);
    font-size: 1.35rem;
    color: var(--neon);
    display: flex; align-items: center; gap: .5rem;
  }
  .nav-links { display: flex; gap: .25rem; }
  .nav-links a {
    padding: .4rem .85rem;
    border-radius: 6px;
    color: var(--muted);
    font-size: .8rem;
    letter-spacing: .05em;
    text-transform: uppercase;
    transition: all .2s;
  }
  .nav-links a:hover, .nav-links a.active {
    background: rgba(0,255,136,.08);
    color: var(--neon);
    text-decoration: none;
  }

  /* ── LAYOUT ── */
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
  .page-header { margin-bottom: 2rem; }
  .page-header h1 {
    font-family: var(--font-disp);
    font-size: 2.2rem;
    color: var(--neon);
    line-height: 1.1;
  }
  .page-header p { color: var(--muted); margin-top: .4rem; }

  /* ── CARDS ── */
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
  }
  .card-header {
    font-size: .7rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
  }

  /* ── STAT CARDS ── */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }
  .stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
  }
  .stat-card.green::before { background: var(--neon); }
  .stat-card.blue::before  { background: var(--neon2); }
  .stat-card.orange::before{ background: var(--orange); }
  .stat-card.purple::before{ background: var(--purple); }
  .stat-label { font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
  .stat-value { font-size: 2rem; font-weight: 700; margin-top: .35rem; }
  .stat-card.green .stat-value  { color: var(--neon); }
  .stat-card.blue .stat-value   { color: var(--neon2); }
  .stat-card.orange .stat-value { color: var(--orange); }
  .stat-card.purple .stat-value { color: var(--purple); }

  /* ── TABLE ── */
  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; font-size: .68rem; letter-spacing: .1em; text-transform: uppercase;
       color: var(--muted); padding: .6rem 1rem; border-bottom: 1px solid var(--border); }
  td { padding: .7rem 1rem; border-bottom: 1px solid rgba(33,38,45,.5);
       font-size: .82rem; vertical-align: middle; }
  tr:hover td { background: rgba(255,255,255,.02); }

  /* ── BADGE ── */
  .badge {
    display: inline-flex; align-items: center; gap: .3rem;
    padding: .2rem .55rem;
    border-radius: 20px;
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .04em;
    border: 1px solid;
  }
  .badge-success  { background: rgba(0,255,136,.08); color: var(--neon);  border-color: rgba(0,255,136,.2); }
  .badge-info     { background: rgba(0,207,255,.08); color: var(--neon2); border-color: rgba(0,207,255,.2); }
  .badge-warning  { background: rgba(255,107,53,.08);color: var(--orange);border-color: rgba(255,107,53,.2); }
  .badge-muted    { background: rgba(139,148,158,.08);color:var(--muted); border-color: rgba(139,148,158,.2); }
  .badge-purple   { background: rgba(191,90,242,.08); color: var(--purple);border-color: rgba(191,90,242,.2); }

  /* ── BUTTONS ── */
  .btn {
    display: inline-flex; align-items: center; gap: .4rem;
    padding: .55rem 1.2rem;
    border-radius: 6px;
    font-family: var(--font-mono);
    font-size: .8rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all .2s;
  }
  .btn-primary {
    background: var(--neon); color: #000;
    border-color: var(--neon);
  }
  .btn-primary:hover { background: #00cc6e; box-shadow: 0 0 20px rgba(0,255,136,.3); }
  .btn-outline {
    background: transparent; color: var(--text);
    border-color: var(--border);
  }
  .btn-outline:hover { border-color: var(--neon); color: var(--neon); }
  .btn-danger {
    background: rgba(239,68,68,.12); color: #f87171;
    border-color: rgba(239,68,68,.25);
  }

  /* ── FORM ── */
  input, textarea, select {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: .85rem;
    padding: .6rem .9rem;
    width: 100%;
    outline: none;
    transition: border-color .2s;
  }
  input:focus, textarea:focus, select:focus { border-color: var(--neon); }
  label { font-size: .75rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: .35rem; display: block; }
  .form-group { margin-bottom: 1.2rem; }

  /* ── UPLOAD ZONE ── */
  .upload-zone {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all .2s;
    position: relative;
  }
  .upload-zone:hover, .upload-zone.drag-over {
    border-color: var(--neon);
    background: rgba(0,255,136,.03);
  }
  .upload-zone input[type=file] {
    position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%;
  }
  .upload-icon { font-size: 3rem; margin-bottom: 1rem; }
  .upload-label { color: var(--muted); font-size: .9rem; }
  .upload-label span { color: var(--neon); }

  /* ── PROGRESS ── */
  .progress-bar { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
  .progress-fill { height: 100%; background: linear-gradient(90deg, var(--neon), var(--neon2)); transition: width .3s; border-radius: 2px; }

  /* ── FOOTER ── */
  footer {
    border-top: 1px solid var(--border);
    text-align: center;
    padding: 1.5rem;
    color: var(--muted);
    font-size: .75rem;
    margin-top: 4rem;
  }

  /* ── GLOW TEXT ── */
  .glow { text-shadow: 0 0 20px rgba(0,255,136,.5); }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* ── TOAST ── */
  #toast {
    position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 8px; padding: .8rem 1.2rem;
    font-size: .82rem; max-width: 320px;
    transform: translateY(100px); opacity: 0;
    transition: all .3s;
    pointer-events: none;
  }
  #toast.show { transform: translateY(0); opacity: 1; }
  #toast.toast-success { border-color: var(--neon); color: var(--neon); }
  #toast.toast-error   { border-color: var(--orange); color: var(--orange); }

  /* ── GRID ── */
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  @media (max-width: 768px) { .two-col { grid-template-columns: 1fr; } }
</style>
"""

NAV_HTML = """
<nav>
  <a href="/" class="nav-brand" style="text-decoration:none">
    <span>🗂️</span> FileOrganizer<span style="color:var(--muted)">Pro</span>
  </a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/organize">Organize</a>
    <a href="/files">Files</a>
    <a href="/history">History</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </div>
</nav>
"""

FOOTER_HTML = """
<footer>
  <p>🗂️ <strong style="color:var(--neon)">FileOrganizer Pro</strong> &nbsp;·&nbsp;
  <a href="/about">About</a> &nbsp;·&nbsp;
  <a href="/contact">Contact</a>
  </p>
</footer>
<div id="toast"></div>
<script>
function showToast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'show toast-' + type;
  setTimeout(() => t.className = '', 3500);
}
// Highlight active nav
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.href === location.href) a.classList.add('active');
});
</script>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════
HOME_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>FileOrganizer Pro</title></head>
<body>
{NAV_HTML}

<!-- HERO -->
<section style="
  min-height: 90vh;
  display: flex; align-items: center;
  background: radial-gradient(ellipse at 30% 50%, rgba(0,255,136,.05) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 20%, rgba(0,207,255,.04) 0%, transparent 55%),
              var(--bg);
  position: relative; overflow: hidden;
">
  <div style="position:absolute;top:10%;right:5%;opacity:.04;font-size:20vw;line-height:1;pointer-events:none">🗂️</div>
  <div class="container" style="text-align:center; padding: 4rem 2rem;">
    <div style="font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;color:var(--neon);margin-bottom:1.5rem">
      ▶ Intelligent File Management System
    </div>
    <h1 style="font-family:var(--font-disp);font-size:clamp(2.5rem,6vw,5rem);line-height:1.05;margin-bottom:1.5rem">
      Stop Drowning in<br>
      <span class="glow" style="color:var(--neon)">Digital Chaos</span>
    </h1>
    <p style="color:var(--muted);font-size:1rem;max-width:540px;margin:0 auto 2.5rem;line-height:1.7">
      FileOrganizer Pro automatically classifies and sorts your files by type, creates structured folder hierarchies, and keeps a full audit trail — all powered by Python.
    </p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="/organize" class="btn btn-primary" style="font-size:.9rem;padding:.75rem 2rem">
        ⚡ Start Organizing
      </a>
      <a href="/dashboard" class="btn btn-outline" style="font-size:.9rem;padding:.75rem 2rem">
        📊 View Dashboard
      </a>
    </div>

    <!-- Live stats pill -->
    <div style="display:inline-flex;gap:2rem;margin-top:3.5rem;padding:1rem 2rem;
                background:var(--card);border:1px solid var(--border);border-radius:40px;
                flex-wrap:wrap;justify-content:center;">
      <div style="text-align:center">
        <div style="font-size:1.5rem;font-weight:700;color:var(--neon)">{{{{ stats.total_files }}}}</div>
        <div style="font-size:.7rem;color:var(--muted);margin-top:.2rem">Files Tracked</div>
      </div>
      <div style="width:1px;background:var(--border)"></div>
      <div style="text-align:center">
        <div style="font-size:1.5rem;font-weight:700;color:var(--neon2)">{{{{ stats.organized_files }}}}</div>
        <div style="font-size:.7rem;color:var(--muted);margin-top:.2rem">Organized</div>
      </div>
      <div style="width:1px;background:var(--border)"></div>
      <div style="text-align:center">
        <div style="font-size:1.5rem;font-weight:700;color:var(--orange)">{{{{ stats.categories|length }}}}</div>
        <div style="font-size:.7rem;color:var(--muted);margin-top:.2rem">Categories</div>
      </div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section style="padding:5rem 0; border-top:1px solid var(--border);">
  <div class="container">
    <div style="text-align:center;margin-bottom:3rem">
      <div style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:.5rem">WHAT IT DOES</div>
      <h2 style="font-family:var(--font-disp);font-size:2rem">Built for Automation</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem">
      {{% for feat in [
        ('🧠','Smart Classification','Detects file type by extension, MIME type, and content — no manual sorting required.','var(--neon)'),
        ('📁','Folder Hierarchy','Creates a clean category-based folder structure: Images, Videos, Code, Documents, and more.','var(--neon2)'),
        ('🗄️','Full Database','Every file and action is stored in SQLite with timestamps, checksums, and full history.','var(--orange)'),
        ('👁️','Auto-Watcher','Monitor any folder in real time — new files are automatically organized the moment they appear.','var(--purple)'),
        ('🔍','Duplicate Detection','MD5 checksum comparison prevents duplicate files from piling up.','var(--neon)'),
        ('📊','Analytics Dashboard','Visualize your file distribution, history timeline, and storage usage at a glance.','var(--neon2)'),
      ] %}}
      <div class="card" style="border-top:2px solid {{{{ feat[3] }}}}">
        <div style="font-size:2rem;margin-bottom:.75rem">{{{{ feat[0] }}}}</div>
        <div style="font-weight:600;margin-bottom:.5rem;color:{{{{ feat[3] }}}}">{{{{ feat[1] }}}}</div>
        <div style="color:var(--muted);line-height:1.6;font-size:.82rem">{{{{ feat[2] }}}}</div>
      </div>
      {{% endfor %}}
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section style="padding:5rem 0; background:var(--surface); border-top:1px solid var(--border);">
  <div class="container">
    <div style="text-align:center;margin-bottom:3rem">
      <h2 style="font-family:var(--font-disp);font-size:2rem">How It Works</h2>
    </div>
    <div style="display:flex;gap:0;flex-wrap:wrap;justify-content:center;">
      {{% for step in [
        ('01','Upload','Drop files or point to a folder — we handle the rest.'),
        ('02','Classify','Content-aware engine assigns each file to the right category.'),
        ('03','Organize','Files are moved/copied into structured category folders.'),
        ('04','Track','Every action is logged to the database with full history.'),
      ] %}}
      <div style="flex:1;min-width:200px;text-align:center;padding:2rem 1rem;position:relative">
        <div style="font-size:3rem;font-weight:800;color:rgba(0,255,136,.12);font-family:var(--font-disp);margin-bottom:.5rem">{{{{ step[0] }}}}</div>
        <div style="font-weight:600;font-size:.95rem;color:var(--neon);margin-bottom:.5rem">{{{{ step[1] }}}}</div>
        <div style="color:var(--muted);font-size:.8rem;line-height:1.6">{{{{ step[2] }}}}</div>
      </div>
      {{% endfor %}}
    </div>
    <div style="text-align:center;margin-top:2rem">
      <a href="/organize" class="btn btn-primary">Get Started →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════════════════
DASHBOARD_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>Dashboard — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container">
  <div class="page-header">
    <h1>Dashboard</h1>
    <p>Real-time overview of your file organization activity</p>
  </div>

  <div class="stats-grid">
    <div class="stat-card green">
      <div class="stat-label">Total Files</div>
      <div class="stat-value">{{{{ stats.total_files }}}}</div>
    </div>
    <div class="stat-card blue">
      <div class="stat-label">Organized</div>
      <div class="stat-value">{{{{ stats.organized_files }}}}</div>
    </div>
    <div class="stat-card orange">
      <div class="stat-label">Storage Used</div>
      <div class="stat-value" style="font-size:1.4rem">{{{{ size_fmt }}}}</div>
    </div>
    <div class="stat-card purple">
      <div class="stat-label">Categories</div>
      <div class="stat-value">{{{{ stats.categories|length }}}}</div>
    </div>
  </div>

  <div class="two-col">
    <!-- Category breakdown -->
    <div class="card">
      <div class="card-header">📂 File Categories</div>
      {{% if stats.categories %}}
      {{% for cat in stats.categories %}}
      <div style="margin-bottom:.8rem">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.25rem">
          <span style="font-size:.85rem">
            {{{{ cat_info[cat.category].icon }}}} {{{{ cat.category }}}}
          </span>
          <span style="color:var(--muted);font-size:.8rem">{{{{ cat.cnt }}}}</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width:{{{{ [(cat.cnt / stats.total_files * 100), 100]|min if stats.total_files else 0 }}}}%;
               background:{{{{ cat_info[cat.category].color }}}}"></div>
        </div>
      </div>
      {{% endfor %}}
      {{% else %}}
      <p style="color:var(--muted);text-align:center;padding:2rem 0">No files organized yet. <a href="/organize">Start now →</a></p>
      {{% endif %}}
    </div>

    <!-- Recent activity -->
    <div class="card">
      <div class="card-header">🕐 Recent Activity</div>
      {{% if stats.recent_activity %}}
      {{% for act in stats.recent_activity %}}
      <div style="padding:.6rem 0;border-bottom:1px solid rgba(33,38,45,.5);display:flex;gap:.75rem;align-items:flex-start">
        <span class="badge {{% if act.status == 'success' %}}badge-success{{% else %}}badge-warning{{% endif %}}">
          {{{{ act.action }}}}
        </span>
        <div style="flex:1;min-width:0">
          <div style="font-size:.82rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{{{ act.file_name }}}}</div>
          <div style="font-size:.7rem;color:var(--muted)">{{{{ act.timestamp }}}}</div>
        </div>
      </div>
      {{% endfor %}}
      {{% else %}}
      <p style="color:var(--muted);text-align:center;padding:2rem 0">No activity yet.</p>
      {{% endif %}}
      <div style="margin-top:1rem">
        <a href="/history" class="btn btn-outline" style="width:100%;justify-content:center">View Full History</a>
      </div>
    </div>
  </div>
</div>
{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# ORGANIZER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
ORGANIZER_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>Organize — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container">
  <div class="page-header">
    <h1>Organize Files</h1>
    <p>Upload files and let the engine classify and sort them automatically</p>
  </div>

  <!-- Settings bar -->
  <div class="card" style="margin-bottom:1.5rem">
    <div class="card-header">⚙️ Organization Settings</div>
    <div style="display:flex;gap:1.5rem;flex-wrap:wrap;align-items:flex-end">
      <div class="form-group" style="margin:0;flex:1;min-width:160px">
        <label>Strategy</label>
        <select id="strategy">
          <option value="copy">Copy (keep original)</option>
          <option value="move">Move (delete original)</option>
        </select>
      </div>
      <div class="form-group" style="margin:0;flex:1;min-width:160px">
        <label>Duplicates</label>
        <select id="duplicates">
          <option value="rename">Rename (add _1, _2…)</option>
          <option value="skip">Skip</option>
          <option value="overwrite">Overwrite</option>
        </select>
      </div>
      <button class="btn btn-outline" onclick="saveSettings()">💾 Save</button>
    </div>
  </div>

  <!-- Drop zone -->
  <div class="upload-zone" id="dropZone">
    <input type="file" id="fileInput" multiple onchange="handleFiles(this.files)">
    <div class="upload-icon">📂</div>
    <div class="upload-label">
      <strong style="color:var(--text);font-size:1rem">Drop files here</strong><br>
      or <span>browse to upload</span>
    </div>
    <div style="color:var(--muted);font-size:.75rem;margin-top:.75rem">
      Supports all file types · Drag & drop multiple files
    </div>
  </div>

  <!-- Preview area -->
  <div id="previewArea" style="display:none;margin-top:1.5rem">
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
        <div class="card-header" style="margin:0">📋 Preview — <span id="fileCount">0</span> files</div>
        <button class="btn btn-primary" id="organizeBtn" onclick="organizeFiles()">⚡ Organize All</button>
      </div>
      <div id="progressWrap" style="display:none;margin-bottom:1rem">
        <div style="font-size:.75rem;color:var(--muted);margin-bottom:.4rem">Processing…</div>
        <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
      </div>
      <table>
        <thead><tr>
          <th>Filename</th><th>Category</th><th>Type</th><th>Status</th>
        </tr></thead>
        <tbody id="previewTable"></tbody>
      </table>
    </div>
  </div>

  <!-- Results -->
  <div id="resultsArea" style="display:none;margin-top:1.5rem">
    <div class="card" style="border-color:var(--neon)">
      <div class="card-header">✅ Organization Complete</div>
      <div style="display:flex;gap:2rem;flex-wrap:wrap">
        <div><span style="font-size:1.5rem;font-weight:700;color:var(--neon)" id="resOrganized">0</span>
          <span style="color:var(--muted);font-size:.8rem;display:block">Organized</span></div>
        <div><span style="font-size:1.5rem;font-weight:700;color:var(--orange)" id="resFailed">0</span>
          <span style="color:var(--muted);font-size:.8rem;display:block">Failed</span></div>
        <div><span style="font-size:1.5rem;font-weight:700;color:var(--muted)" id="resTotal">0</span>
          <span style="color:var(--muted);font-size:.8rem;display:block">Total</span></div>
      </div>
      <div style="margin-top:1rem;display:flex;gap:.75rem">
        <a href="/files" class="btn btn-outline">📁 View Files</a>
        <a href="/dashboard" class="btn btn-outline">📊 Dashboard</a>
        <button class="btn btn-outline" onclick="resetForm()">🔄 Organize More</button>
      </div>
    </div>
  </div>
</div>

<script>
let selectedFiles = [];

// Drag & drop
const dz = document.getElementById('dropZone');
['dragover','dragenter'].forEach(e => dz.addEventListener(e, ev => {{ ev.preventDefault(); dz.classList.add('drag-over'); }}));
['dragleave','drop'].forEach(e => dz.addEventListener(e, ev => {{ ev.preventDefault(); dz.classList.remove('drag-over'); }}));
dz.addEventListener('drop', ev => handleFiles(ev.dataTransfer.files));

async function handleFiles(files) {{
  selectedFiles = Array.from(files);
  if (!selectedFiles.length) return;

  // Preview
  const names = selectedFiles.map(f => f.name);
  const resp = await fetch('/api/preview', {{
    method: 'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{filenames: names}})
  }});
  const data = await resp.json();

  document.getElementById('fileCount').textContent = selectedFiles.length;
  const tbody = document.getElementById('previewTable');
  tbody.innerHTML = '';
  data.preview.forEach(p => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td style="max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${{p.filename}}</td>
      <td><span class="badge badge-info">${{p.icon}} ${{p.category}}</span></td>
      <td><span style="color:var(--muted)">${{p.file_type}}</span></td>
      <td id="status-${{p.filename.replace(/[^a-z0-9]/gi,'_')}}">
        <span class="badge badge-muted">pending</span>
      </td>`;
    tbody.appendChild(tr);
  }});

  document.getElementById('previewArea').style.display = 'block';
  document.getElementById('resultsArea').style.display = 'none';
}}

async function organizeFiles() {{
  if (!selectedFiles.length) return;
  const btn = document.getElementById('organizeBtn');
  btn.disabled = true; btn.textContent = '⏳ Processing…';
  document.getElementById('progressWrap').style.display = 'block';

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append('files', f));

  const resp = await fetch('/api/upload', {{ method: 'POST', body: formData }});
  const data = await resp.json();

  document.getElementById('progressFill').style.width = '100%';

  // Update statuses
  data.results.forEach(r => {{
    const key = r.filename.replace(/[^a-z0-9]/gi,'_');
    const cell = document.getElementById('status-' + key);
    if (cell) {{
      cell.innerHTML = r.success
        ? `<span class="badge badge-success">✓ ${{r.category}}</span>`
        : `<span class="badge badge-warning">✗ failed</span>`;
    }}
  }});

  document.getElementById('resOrganized').textContent = data.organized;
  document.getElementById('resFailed').textContent = data.total - data.organized;
  document.getElementById('resTotal').textContent = data.total;
  document.getElementById('resultsArea').style.display = 'block';
  btn.textContent = '✅ Done';
  showToast(`${{data.organized}} files organized successfully!`);
}}

function resetForm() {{
  selectedFiles = [];
  document.getElementById('previewArea').style.display = 'none';
  document.getElementById('resultsArea').style.display = 'none';
  document.getElementById('progressFill').style.width = '0%';
  document.getElementById('progressWrap').style.display = 'none';
  document.getElementById('organizeBtn').disabled = false;
  document.getElementById('organizeBtn').textContent = '⚡ Organize All';
  document.getElementById('fileInput').value = '';
}}

async function saveSettings() {{
  await fetch('/api/settings', {{
    method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{
      duplicate_handling: document.getElementById('duplicates').value,
    }})
  }});
  showToast('Settings saved');
}}

// Load settings on mount
fetch('/api/settings').then(r=>r.json()).then(s => {{
  if (s.duplicate_handling) document.getElementById('duplicates').value = s.duplicate_handling;
}});
</script>
{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# FILES PAGE
# ═══════════════════════════════════════════════════════════════════════════════
FILES_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>Files — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container">
  <div class="page-header">
    <h1>File Library</h1>
    <p>All tracked files with filtering and search</p>
  </div>

  <!-- Filters -->
  <div class="card" style="margin-bottom:1.5rem">
    <form method="GET" action="/files" style="display:flex;gap:1rem;flex-wrap:wrap;align-items:flex-end">
      <div class="form-group" style="margin:0;flex:1;min-width:160px">
        <label>Category</label>
        <select name="category" onchange="this.form.submit()">
          <option value="">All Categories</option>
          {{% for cat in categories %}}
          <option value="{{{{ cat }}}}" {{% if cat == selected_cat %}}selected{{% endif %}}>{{{{ cat }}}}</option>
          {{% endfor %}}
        </select>
      </div>
      <div class="form-group" style="margin:0;flex:1;min-width:140px">
        <label>Status</label>
        <select name="status" onchange="this.form.submit()">
          <option value="">All Statuses</option>
          <option value="organized" {{% if selected_status=='organized' %}}selected{{% endif %}}>Organized</option>
          <option value="pending"   {{% if selected_status=='pending'   %}}selected{{% endif %}}>Pending</option>
          <option value="failed"    {{% if selected_status=='failed'    %}}selected{{% endif %}}>Failed</option>
          <option value="skipped"   {{% if selected_status=='skipped'   %}}selected{{% endif %}}>Skipped</option>
        </select>
      </div>
      {{% if selected_cat or selected_status %}}
      <a href="/files" class="btn btn-outline">✕ Clear</a>
      {{% endif %}}
    </form>
  </div>

  <div class="card">
    {{% if files %}}
    <table>
      <thead><tr>
        <th>#</th><th>Filename</th><th>Category</th><th>Type</th><th>Size</th><th>Status</th><th>Date</th>
      </tr></thead>
      <tbody>
        {{% for f in files %}}
        <tr>
          <td style="color:var(--muted)">{{{{ f.id }}}}</td>
          <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">
            <span title="{{{{ f.original_path }}}}">{{{{ f.original_name }}}}</span>
          </td>
          <td><span class="badge badge-info" style="border-color:{{{{ f.color }}}}20;color:{{{{ f.color }}}}">
            {{{{ f.icon }}}} {{{{ f.category }}}}
          </span></td>
          <td><span style="color:var(--muted)">{{{{ f.file_type }}}}</span></td>
          <td style="color:var(--muted)">{{{{ f.size_fmt }}}}</td>
          <td>
            <span class="badge
              {{% if f.status=='organized' %}}badge-success
              {{% elif f.status=='failed' %}}badge-warning
              {{% elif f.status=='skipped' %}}badge-muted
              {{% else %}}badge-info{{% endif %}}">
              {{{{ f.status }}}}
            </span>
          </td>
          <td style="color:var(--muted)">{{{{ f.created_at[:16] }}}}</td>
        </tr>
        {{% endfor %}}
      </tbody>
    </table>
    <!-- Pagination -->
    <div style="display:flex;gap:.5rem;justify-content:flex-end;margin-top:1rem;align-items:center">
      {{% if page > 1 %}}
      <a href="?page={{{{ page-1 }}}}&category={{{{ selected_cat }}}}&status={{{{ selected_status }}}}" class="btn btn-outline" style="padding:.4rem .8rem">← Prev</a>
      {{% endif %}}
      <span style="color:var(--muted);font-size:.8rem">Page {{{{ page }}}}</span>
      {{% if files|length == 30 %}}
      <a href="?page={{{{ page+1 }}}}&category={{{{ selected_cat }}}}&status={{{{ selected_status }}}}" class="btn btn-outline" style="padding:.4rem .8rem">Next →</a>
      {{% endif %}}
    </div>
    {{% else %}}
    <div style="text-align:center;padding:3rem;color:var(--muted)">
      No files found. <a href="/organize">Start organizing →</a>
    </div>
    {{% endif %}}
  </div>
</div>
{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# HISTORY PAGE
# ═══════════════════════════════════════════════════════════════════════════════
HISTORY_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>History — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container">
  <div class="page-header">
    <h1>Activity History</h1>
    <p>Full audit trail of every file operation</p>
  </div>
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div class="card-header" style="margin:0">{{{{ history|length }}}} entries</div>
      <input type="text" id="search" placeholder="Search history…" style="width:260px" oninput="filterHistory(this.value)">
    </div>
    {{% if history %}}
    <table id="histTable">
      <thead><tr>
        <th>#</th><th>Action</th><th>File</th><th>Category</th><th>Details</th><th>Status</th><th>Time</th>
      </tr></thead>
      <tbody>
        {{% for h in history %}}
        <tr class="hist-row">
          <td style="color:var(--muted)">{{{{ h.id }}}}</td>
          <td><span class="badge
            {{% if h.action=='copy' %}}badge-info
            {{% elif h.action=='move' %}}badge-purple
            {{% elif h.action=='skip' %}}badge-muted
            {{% else %}}badge-warning{{% endif %}}">
            {{{{ h.action }}}}
          </span></td>
          <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{{{ h.file_name }}}}</td>
          <td style="color:var(--muted)">{{{{ h.category or '—' }}}}</td>
          <td style="color:var(--muted);font-size:.78rem">{{{{ h.details or '—' }}}}</td>
          <td><span class="badge {{% if h.status=='success' %}}badge-success{{% else %}}badge-warning{{% endif %}}">{{{{ h.status }}}}</span></td>
          <td style="color:var(--muted);font-size:.78rem;white-space:nowrap">{{{{ h.timestamp[:16] }}}}</td>
        </tr>
        {{% endfor %}}
      </tbody>
    </table>
    {{% else %}}
    <div style="text-align:center;padding:3rem;color:var(--muted)">No history yet. <a href="/organize">Start organizing →</a></div>
    {{% endif %}}
  </div>
</div>
<script>
function filterHistory(q) {{
  q = q.toLowerCase();
  document.querySelectorAll('.hist-row').forEach(row => {{
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
</script>
{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════════════════════════════════════
ABOUT_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>About — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container" style="max-width:860px">
  <div class="page-header">
    <h1>About This Project</h1>
    <p>An intelligent file organization system built with Python</p>
  </div>

  <div class="card" style="margin-bottom:1.5rem;border-left:3px solid var(--neon);padding-left:2rem">
    <p style="font-family:var(--font-disp);font-size:1.2rem;line-height:1.7;color:var(--text)">
      FileOrganizer Pro is an open-source automation tool that eliminates the tedium of manual file management
      through intelligent content-based classification and Python-powered automation.
    </p>
  </div>

  <div class="two-col" style="margin-bottom:1.5rem">
    <div class="card">
      <div class="card-header">🏗️ Architecture</div>
      <p style="color:var(--muted);line-height:1.8;font-size:.85rem">
        Built on a <strong style="color:var(--text)">modular Python architecture</strong> with clean separation of concerns:
        classification, organization, database, routing, and file watching are all independent modules that
        communicate through well-defined interfaces.
      </p>
    </div>
    <div class="card">
      <div class="card-header">🛠️ Tech Stack</div>
      <div style="display:flex;flex-direction:column;gap:.5rem">
        {{% for tech, desc in [
          ('Python 3.10+','Core language'),
          ('Flask','Web framework & REST API'),
          ('SQLite','Embedded database'),
          ('JetBrains Mono','Monospace font'),
          ('Playfair Display','Display font'),
        ] %}}
        <div style="display:flex;justify-content:space-between;padding:.4rem 0;border-bottom:1px solid var(--border)">
          <span style="color:var(--neon);font-weight:600">{{{{ tech }}}}</span>
          <span style="color:var(--muted);font-size:.8rem">{{{{ desc }}}}</span>
        </div>
        {{% endfor %}}
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:1.5rem">
    <div class="card-header">📦 Module Overview</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem">
      {{% for mod, desc, color in [
        ('app.py','Application factory & entry point','var(--neon)'),
        ('modules/classifier.py','Content-aware file classification engine','var(--neon2)'),
        ('modules/organizer.py','Core file organization & folder logic','var(--orange)'),
        ('modules/database.py','SQLite schema, CRUD, and query helpers','var(--purple)'),
        ('modules/routes.py','All Flask routes and API endpoints','var(--neon)'),
        ('modules/watcher.py','Polling-based folder auto-watcher','var(--neon2)'),
        ('templates/html_templates.py','All HTML pages as Python strings','var(--orange)'),
      ] %}}
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1rem;border-top:2px solid {{{{ color }}}}">
        <div style="font-size:.78rem;font-weight:700;color:{{{{ color }}}};margin-bottom:.35rem">{{{{ mod }}}}</div>
        <div style="font-size:.75rem;color:var(--muted);line-height:1.5">{{{{ desc }}}}</div>
      </div>
      {{% endfor %}}
    </div>
  </div>

  <div class="card">
    <div class="card-header">🚀 Getting Started</div>
    <pre style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;overflow-x:auto;font-size:.8rem;line-height:1.8;color:var(--neon2)">
# 1. Install dependencies
pip install flask

# 2. Run the application
python app.py

# 3. Open in browser
open http://localhost:5000
    </pre>
    <div style="margin-top:1rem">
      <a href="/organize" class="btn btn-primary">⚡ Start Organizing</a>
      <a href="/contact" class="btn btn-outline" style="margin-left:.75rem">📩 Contact Us</a>
    </div>
  </div>
</div>
{FOOTER_HTML}
</body></html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# CONTACT PAGE
# ═══════════════════════════════════════════════════════════════════════════════
CONTACT_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>{BASE_STYLE}<title>Contact — FileOrganizer Pro</title></head>
<body>
{NAV_HTML}
<div class="container" style="max-width:660px">
  <div class="page-header">
    <h1>Contact Us</h1>
    <p>Have a question, bug report, or feature request?</p>
  </div>

  <div class="card" style="margin-bottom:1.5rem">
    <div class="card-header">📩 Send a Message</div>
    <div class="form-group">
      <label>Your Name</label>
      <input type="text" id="name" placeholder="Ada Lovelace">
    </div>
    <div class="form-group">
      <label>Email Address</label>
      <input type="email" id="email" placeholder="ada@example.com">
    </div>
    <div class="form-group">
      <label>Subject</label>
      <select id="subject">
        <option>Bug Report</option>
        <option>Feature Request</option>
        <option>General Question</option>
        <option>Other</option>
      </select>
    </div>
    <div class="form-group">
      <label>Message</label>
      <textarea id="message" rows="5" placeholder="Describe your issue or idea…"></textarea>
    </div>
    <button class="btn btn-primary" onclick="submitContact()" style="width:100%;justify-content:center;padding:.75rem">
      📤 Send Message
    </button>
    <div id="contactResult" style="margin-top:1rem;display:none"></div>
  </div>

  <div class="two-col">
    <div class="card" style="border-top:2px solid var(--neon)">
      <div style="font-size:1.5rem;margin-bottom:.5rem">💡</div>
      <div style="font-weight:600;color:var(--neon);margin-bottom:.35rem">FAQ</div>
      <div style="color:var(--muted);font-size:.82rem;line-height:1.7">
        Common questions are covered in the About page — including setup, supported file types, and how the watcher works.
      </div>
      <a href="/about" class="btn btn-outline" style="margin-top:.75rem;font-size:.75rem">View FAQ →</a>
    </div>
    <div class="card" style="border-top:2px solid var(--neon2)">
      <div style="font-size:1.5rem;margin-bottom:.5rem">📖</div>
      <div style="font-weight:600;color:var(--neon2);margin-bottom:.35rem">Docs</div>
      <div style="color:var(--muted);font-size:.82rem">Read the full documentation on the About page.</div>
      <a href="/about" class="btn btn-outline" style="margin-top:.75rem;font-size:.75rem">Read Docs →</a>
    </div>
  </div>
</div>

<script>
async function submitContact() {{
  const name    = document.getElementById('name').value.trim();
  const email   = document.getElementById('email').value.trim();
  const message = document.getElementById('message').value.trim();
  if (!name || !email || !message) {{
    showToast('Please fill in all required fields', 'error'); return;
  }}
  const resp = await fetch('/api/contact', {{
    method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{ name, email, message }})
  }});
  const data = await resp.json();
  const res = document.getElementById('contactResult');
  res.style.display = 'block';
  res.style.color = data.success ? 'var(--neon)' : 'var(--orange)';
  res.textContent = data.message;
  if (data.success) {{
    document.getElementById('name').value = '';
    document.getElementById('email').value = '';
    document.getElementById('message').value = '';
    showToast('Message sent!');
  }}
}}
</script>
{FOOTER_HTML}
</body></html>"""