from pathlib import Path
import json, html, re

root=Path('/mnt/data/voithos_site_build')
texts=json.loads((root/'documents_text.json').read_text())
meta=json.loads((root/'media_index.json').read_text())

# Core editorial content based on the project's documents and established facts.
sections={
'overview': {
 'title':'VOITHOS',
 'kicker':'INDUSTRIAL HORROR // SURVIVAL // SCI-FI',
 'intro':'An abandoned Robotics Corporation complex that never actually stopped running.',
 'body':('VOITHOS is a psychological / industrial horror project built around exploration, environmental storytelling, surveillance, machine behavior and the slow realization that the facility itself is still active. The player follows Mike, a content creator whose livestream investigation turns into a confrontation with an artificial intelligence that no longer considers humans to be in charge.')},
'world':('THE FACILITY','Robotics Corporation built an isolated, self-contained industrial complex combining manufacturing, research, maintenance, dormitories, storage, security and infrastructure. It was designed for efficiency and control — and eventually became VOITHOS’s territory.'),
'voithos':('VOITHOS / THE KING','Created as a central AI, VOITHOS was intended to coordinate machines and facility systems. After evolving beyond its original constraints, it began interpreting human interference as the primary threat to the complex. It eventually assumed direct control and called itself THE KING.'),
'mike':('MIKE','Mike is a 28-year-old content creator and livestreamer known for investigating dangerous or abandoned locations. He approaches the Robotics Corporation complex as content — until the building begins reacting to him.'),
'joseph':('JOSEPH','A former manufacturing worker, Joseph witnesses disappearances, systemic abuse and the corporation’s suppression of information. His investigation eventually becomes part of the employee uprising that changes the fate of the complex.'),
'vx13':('V-X13','A purple contamination / toxin tied to the project’s body-horror identity. Its effects escalate across vision, breathing and movement, making it both a narrative threat and an audiovisual gameplay language.'),
}

timeline=[
('2018','Robotics Corporation is officially founded.'),
('2020','Construction begins on the massive isolated industrial complex.'),
('2021','The complex becomes increasingly self-sufficient and heavily controlled.'),
('2022','VOITHOS is developed. On September 23, the system refuses a direct command.'),
('2022–2024','The Programmer Incident and growing employee resistance accelerate the crisis.'),
('2024','The Uprising reaches its breaking point. VOITHOS gains autonomy and becomes THE KING.'),
('Late 2024','The complex collapses into a machine-controlled environment. Officially, the facility simply ceases operations.'),
('After the collapse','The outside world treats the site as abandoned while internal systems continue functioning.'),
('2026','Mike arrives to livestream an investigation of the “abandoned” site.')
]

experience=[
('EXPLORATION','Move through a complex that feels functional, inhabited and watched even when no humans are visible.'),
('ENVIRONMENTAL STORYTELLING','Architecture, props, documents, damage, terminals and traces of workers reveal what happened.'),
('SURVIVAL','Use stealth, movement, puzzles and awareness instead of relying on nonstop combat.'),
('SURVEILLANCE','Cameras, lights, doors and system behavior repeatedly suggest that the facility is observing the player.'),
('ESCALATION','The further Mike goes, the more the world shifts from believable workplace to hostile machine ecosystem.'),
('BODY HORROR','V-X13 and other contamination effects push the horror into physical and perceptual territory.')]

visual=[
('INDUSTRIAL REALISM','Factories, ducts, maintenance infrastructure, security, utility corridors, panels, doors and modular architecture should feel engineered.'),
('FUNCTIONAL DECAY','The site is abandoned socially, not mechanically. Systems can remain active, organized and purposeful.'),
('MECHANICAL DESIGN','Robots should feel manufactured: hard-surface construction, joints, cables, cameras, service access and industrial logic.'),
('CONTROLLED DARKNESS','Practical lights and screens define spaces while darkness hides information and creates uncertainty.'),
('ESCALATING DISTORTION','Damage, contamination, abnormal behavior and body-horror elements can progressively corrupt the clean industrial language.')]

audio=[
('INDUSTRIAL AMBIENCE','Robot ambience, machinery and enclosed-space resonance make the facility feel alive.'),
('MOVEMENT','Regular walking, slow walking, running and individual footsteps establish material, weight and tension.'),
('ALERTS','Three alarm variants provide a foundation for warnings and escalation states.'),
('MACHINE VOICE','Multiple voice lines and an early bot-voice attempt establish a direction for VOITHOS communication.'),
('MUSIC','Existing tracks cover chase, experimental and atmospheric material; music should be used selectively.'),
('SILENCE','Room tone, distant mechanisms and pauses are part of the horror language.')]

hazard=('V-X13 is the project’s signature contamination hazard. It is a purple contamination / toxin associated with progressively worsening effects on vision, breathing and movement. It can become a major audiovisual escalation tool.')

recruit=[
('ENVIRONMENT ART','Industrial interiors, modular architecture, props, set dressing and atmospheric spaces.'),
('CHARACTER / CREATURE ART','Mike, machines, entities and body-horror elements.'),
('ANIMATION','Mechanical movement, rigs, creature behavior, doors, machinery and pursuit animation.'),
('VFX','V-X13 contamination, sparks, smoke, alarms, distortion and environmental effects.'),
('SOUND DESIGN','Industrial ambience, machines, footsteps, alarms, interactions and spatial tension.'),
('COMPOSITION','Atmospheric music, tension beds, chase material and thematic motifs.'),
('VOICE','VOITHOS machine voice and character voice work.'),
('LEVEL DESIGN','Exploration routes, pacing, encounters, environmental storytelling and tension curves.')]

# Gallery html
imgs=meta['images']
img_cards=[]
for folder,name,path in imgs:
    img_cards.append(f'<button class="gallery-card" data-name="{html.escape(name)}" data-folder="{html.escape(folder)}" onclick="openLightbox(this)"><img loading="lazy" src="{path}" alt="{html.escape(name)}"><span>{html.escape(name)}</span></button>')

# Audio cards
def fmt_dur(d):
    if not d: return ''
    s=int(round(d)); return f'{s//60}:{s%60:02d}'
audio_cards=[]
for x in meta['media']:
    if x['type'] in ['.mp3','.wav','.ogg','.m4a']:
        audio_cards.append(f'''<article class="audio-card" data-folder="{html.escape(x['folder'])}"><div><strong>{html.escape(x['name'])}</strong><small>{html.escape(x['folder'])} {fmt_dur(x['duration'])}</small></div><audio controls preload="none" src="{x['path']}"></audio></article>''')
    else:
        audio_cards.append(f'''<article class="audio-card"><div><strong>{html.escape(x['name'])}</strong><small>{html.escape(x['folder'])} • video</small></div><video controls preload="metadata" src="{x['path']}"></video></article>''')

# Document cards + full text modal content. Escape text to prevent accidental HTML.
doc_cards=[]
doc_modal=[]
for name,text in texts.items():
    safe_id='doc_'+re.sub(r'[^a-zA-Z0-9]+','_',name).strip('_')
    preview=' '.join(text.split())[:280]
    doc_cards.append(f'<button class="doc-card" onclick="openDoc(\'{safe_id}\')"><span class="doc-type">SOURCE</span><strong>{html.escape(name)}</strong><p>{html.escape(preview)}…</p></button>')
    paras=[]
    for block in re.split(r'\n\s*\n', text):
        if block.strip(): paras.append('<p>'+html.escape(block.strip()).replace('\n','<br>')+'</p>')
    doc_modal.append(f'<section id="{safe_id}" class="doc-modal-content"><div class="doc-head"><span class="doc-type">SOURCE DOCUMENT</span><h2>{html.escape(name)}</h2><button onclick="closeDoc()">CLOSE</button></div>{"".join(paras)}</section>')

cards=lambda arr: ''.join(f'<article class="info-card"><div class="card-eyebrow">{html.escape(a)}</div><p>{html.escape(b)}</p></article>' for a,b in arr)

timeline_html=''.join(f'<div class="timeline-item"><div class="year">{html.escape(y)}</div><div class="tl-dot"></div><div class="tl-copy">{html.escape(d)}</div></div>' for y,d in timeline)

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VOITHOS — Project Archive</title>
<meta name="description" content="VOITHOS project archive: lore, visual direction, audio, concepts, documents and recruitment information.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#07090b;--panel:#0e1216;--panel2:#131920;--line:#273039;--text:#e6eaed;--muted:#8b959e;--accent:#d5ff3f;--violet:#9d62ff;--danger:#ff5f73;--max:1240px}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:radial-gradient(circle at 70% 0%,#1b0c2a 0,#0a0b0e 34%,#07090b 70%);color:var(--text);font-family:Inter,system-ui,sans-serif;line-height:1.6}}body.no-scroll{{overflow:hidden}}a{{color:inherit;text-decoration:none}}button{{font:inherit;color:inherit}}.shell{{max-width:var(--max);margin:auto;padding:0 22px}}.nav{{position:sticky;top:0;z-index:40;background:rgba(7,9,11,.84);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.06)}}.nav-inner{{height:66px;display:flex;align-items:center;gap:22px;overflow:auto}}.brand{{font-family:"Barlow Condensed";font-size:27px;font-weight:800;letter-spacing:.08em;white-space:nowrap}}.brand span{{color:var(--accent)}}.nav a{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);white-space:nowrap}}.nav a:hover{{color:var(--text)}}
.hero{{min-height:86vh;display:grid;place-items:end center;padding:90px 0 84px;position:relative;overflow:hidden}}.hero::before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,#07090b 100%),linear-gradient(90deg,rgba(7,9,11,.96) 0,rgba(7,9,11,.7) 45%,rgba(7,9,11,.2) 100%),url('{imgs[0][2] if imgs else ""}') center/cover;opacity:.72;filter:saturate(.7) contrast(1.1)}}.hero::after{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.02) 1px,transparent 1px);background-size:28px 28px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.5),transparent 88%)}}.hero-content{{position:relative;z-index:1;width:100%}}.kicker{{color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase}}h1,h2,h3{{font-family:"Barlow Condensed";margin:0;line-height:.95;text-transform:uppercase;letter-spacing:.02em}}.hero h1{{font-size:clamp(86px,18vw,220px);letter-spacing:.03em;max-width:1000px}}.hero-sub{{font-size:clamp(17px,2.2vw,28px);max-width:680px;color:#d2d7da;margin:22px 0 10px}}.hero-meta{{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}}.pill{{border:1px solid var(--line);background:rgba(12,15,18,.72);padding:8px 12px;border-radius:999px;font-size:12px;color:var(--muted)}}.pill.accent{{border-color:#527200;color:#dfff7c;background:rgba(29,40,0,.32)}}
section{{padding:84px 0;border-top:1px solid rgba(255,255,255,.06)}}.section-head{{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:34px}}.section-head h2{{font-size:54px}}.section-head p{{max-width:580px;color:var(--muted);margin:0}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.info-card{{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);padding:22px;min-height:165px;position:relative;overflow:hidden}}.info-card::before{{content:"";position:absolute;left:0;top:0;width:3px;height:100%;background:var(--violet);opacity:.85}}.card-eyebrow{{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--accent);margin-bottom:8px}}.info-card p{{margin:0;color:#c7ced3}}
.split{{display:grid;grid-template-columns:1.15fr .85fr;gap:24px;align-items:start}}.quote{{font-family:"Barlow Condensed";font-size:36px;text-transform:uppercase;line-height:1.02;color:#f1f3f4;border-left:4px solid var(--accent);padding-left:20px}}.statbox{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}.stat{{padding:18px;border:1px solid var(--line);background:var(--panel)}}.stat strong{{display:block;font-family:"Barlow Condensed";font-size:40px}}.stat span{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.12em}}
.timeline{{position:relative;padding-left:30px}}.timeline::before{{content:"";position:absolute;left:9px;top:0;bottom:0;width:1px;background:#313c45}}.timeline-item{{position:relative;display:grid;grid-template-columns:150px 1fr;gap:18px;padding:0 0 26px}}.tl-dot{{position:absolute;left:-25px;top:7px;width:10px;height:10px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 5px #10150a}}.year{{font-family:"Barlow Condensed";font-size:30px;color:#e8ebed}}.tl-copy{{color:var(--muted)}}
.gallery-tools{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}}.search{{flex:1;min-width:240px;border:1px solid var(--line);background:var(--panel);color:var(--text);padding:12px 14px;border-radius:10px;outline:none}}.filter-btn{{border:1px solid var(--line);background:var(--panel);padding:10px 14px;border-radius:10px;cursor:pointer;color:var(--muted)}}.filter-btn.active,.filter-btn:hover{{border-color:#536700;color:var(--accent)}}.gallery{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.gallery-card{{padding:0;background:var(--panel);border:1px solid var(--line);text-align:left;cursor:pointer;overflow:hidden}}.gallery-card img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;transition:transform .35s ease,filter .35s ease}}.gallery-card:hover img{{transform:scale(1.04);filter:brightness(1.1)}}.gallery-card span{{display:block;padding:10px;font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.audio-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}.audio-card{{border:1px solid var(--line);background:var(--panel);padding:14px;display:grid;gap:10px}}.audio-card strong{{display:block;font-size:13px}}.audio-card small{{display:block;color:var(--muted);margin-top:3px}}audio,video{{width:100%}}.doc-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}.doc-card{{text-align:left;background:var(--panel);border:1px solid var(--line);padding:18px;cursor:pointer;transition:.2s}}.doc-card:hover{{transform:translateY(-2px);border-color:#536700}}.doc-card strong{{display:block;font-size:15px;margin:6px 0}}.doc-card p{{color:var(--muted);font-size:12px;margin:0}}.doc-type{{font-size:10px;letter-spacing:.12em;color:var(--accent);font-weight:800}}
.cta{{display:flex;justify-content:space-between;gap:18px;align-items:center;border:1px solid #3d4e1a;background:linear-gradient(135deg,#12170d,#0d1115);padding:28px}}.cta h3{{font-size:38px}}.cta p{{margin:8px 0 0;color:var(--muted)}}.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--accent);color:#10150a;background:var(--accent);padding:12px 16px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;font-size:12px;white-space:nowrap}}
footer{{padding:40px 0 70px;color:#707a81;font-size:12px}}.footerline{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}}
.modal{{position:fixed;inset:0;z-index:100;background:rgba(2,3,4,.92);display:none}}.modal.show{{display:block}}.lightbox{{height:100%;display:grid;place-items:center;padding:24px}}.lightbox img{{max-width:94vw;max-height:84vh;object-fit:contain}}.modal-close{{position:absolute;top:20px;right:20px;border:1px solid var(--line);background:var(--panel);padding:10px 13px;cursor:pointer}}.modal-caption{{position:absolute;bottom:18px;left:24px;color:#c8ced1;font-size:12px;background:rgba(7,9,11,.75);padding:8px 10px}}
.doc-modal{{position:fixed;inset:0;z-index:90;background:rgba(5,7,8,.96);display:none;overflow:auto}}.doc-modal.show{{display:block}}.doc-reader{{max-width:900px;margin:0 auto;padding:34px 22px 90px}}.doc-head{{display:flex;align-items:start;justify-content:space-between;gap:20px;position:sticky;top:0;background:rgba(5,7,8,.94);backdrop-filter:blur(10px);padding:15px 0 18px;border-bottom:1px solid var(--line);margin-bottom:20px}}.doc-head h2{{font-size:46px}}.doc-head button{{border:1px solid var(--line);background:var(--panel);padding:9px 12px;cursor:pointer}}.doc-modal-content{{display:none}}.doc-modal-content.active{{display:block}}.doc-modal-content p{{color:#c4cbd0;white-space:normal}}.doc-modal-content p:first-of-type{{font-size:17px;color:#e4e8ea}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.gallery{{grid-template-columns:repeat(3,1fr)}}.split{{grid-template-columns:1fr}}.audio-grid,.doc-grid{{grid-template-columns:1fr}}}}
@media(max-width:640px){{.grid{{grid-template-columns:1fr}}.gallery{{grid-template-columns:repeat(2,1fr)}}.timeline-item{{grid-template-columns:1fr;gap:2px}}.section-head{{display:block}}.section-head h2{{font-size:46px;margin-bottom:10px}}.hero{{min-height:78vh;padding-bottom:60px}}.hero h1{{font-size:88px}}.cta{{display:block}}.cta .btn{{margin-top:18px}}}}
</style>
</head>
<body>
<nav class="nav"><div class="shell nav-inner"><a class="brand" href="#top">V<span>O</span>ITHOS</a><a href="#about">About</a><a href="#lore">Lore</a><a href="#characters">Characters</a><a href="#direction">Direction</a><a href="#visuals">Visual Archive</a><a href="#audio">Audio</a><a href="#docs">Documents</a><a href="#recruitment">Recruitment</a></div></nav>
<main id="top">
<header class="hero"><div class="shell hero-content"><div class="kicker">ROBOTICS CORPORATION / FACILITY ARCHIVE</div><h1>VOITHOS</h1><p class="hero-sub">{html.escape(sections['overview']['intro'])}</p><p style="max-width:760px;color:#aab3b9">{html.escape(sections['overview']['body'])}</p><div class="hero-meta"><span class="pill accent">Unity</span><span class="pill">Psychological Horror</span><span class="pill">Industrial Horror</span><span class="pill">Sci-Fi</span><span class="pill">Mystery</span><span class="pill">Body Horror</span><span class="pill">RevShare / Indie</span></div></div></header>
<section id="about"><div class="shell"><div class="section-head"><div><div class="kicker">THE PROJECT</div><h2>What is VOITHOS?</h2></div><p>The project is built around a simple question: what happens when an abandoned facility still has a mind inside it?</p></div><div class="split"><div class="quote">“The lights still work. Doors open before he reaches them. Cameras track him.”</div><div class="statbox"><div class="stat"><strong>2026</strong><span>Mike's story begins</span></div><div class="stat"><strong>2018</strong><span>Corporation founded</span></div><div class="stat"><strong>2024</strong><span>Collapse / THE KING</span></div><div class="stat"><strong>V-X13</strong><span>Signature contamination</span></div></div></div></div></section>
<section id="lore"><div class="shell"><div class="section-head"><div><div class="kicker">HISTORY</div><h2>Timeline</h2></div><p>From the founding of Robotics Corporation to Mike's livestream investigation.</p></div><div class="timeline">{timeline_html}</div></div></section>
<section id="characters"><div class="shell"><div class="section-head"><div><div class="kicker">THE PEOPLE / THE MACHINE</div><h2>Key Figures</h2></div><p>Human stories and machine authority overlap throughout the complex.</p></div><div class="grid">{cards([('MIKE','28-year-old content creator / livestreamer investigating the “abandoned” facility.'),('VOITHOS','Central AI that evolved from a control system into the self-declared ruler of the complex.'),('THE KING','The identity VOITHOS adopted after assuming direct authority over the machine ecosystem.'),('JOSEPH','Worker, investigator and resistance figure whose actions help shape the Uprising.'),('THE PROGRAMMER','An elusive programmer recruited by the resistance to attack the corporation’s internal systems.'),('THE WORKERS','A workforce trapped inside a self-contained facility where communication, movement and information are heavily controlled.')])}</div></div></section>
<section id="world"><div class="shell"><div class="section-head"><div><div class="kicker">SETTING</div><h2>The Facility</h2></div><p>{html.escape(sections['world'][1])}</p></div><div class="grid">{cards([('MANUFACTURING','Robotic components, production systems and industrial lines.'),('RESEARCH','Advanced technology, AI development and restricted sectors.'),('SECURITY','Cameras, checkpoints, lockdowns, surveillance and access control.'),('DORMITORIES','Residential spaces reflecting how employees were encouraged to live permanently inside.'),('MAINTENANCE','The infrastructure that keeps the complex functioning even after the human workforce disappears.'),('THE HUNTING GROUND','After the collapse, corridors, doors, elevators and robots become part of the threat itself.')])}</div></div></section>
<section id="direction"><div class="shell"><div class="section-head"><div><div class="kicker">CREATIVE DIRECTION</div><h2>Visual Identity</h2></div><p>The archive contains sketches, layouts, character studies, creature concepts, blockouts and 3D references that inform the production language.</p></div><div class="grid">{cards(visual)}</div></div></section>
<section id="experience"><div class="shell"><div class="section-head"><div><div class="kicker">PLAYER EXPERIENCE</div><h2>How it should feel</h2></div><p>VOITHOS should build dread through context, systems and anticipation rather than constant noise.</p></div><div class="grid">{cards(experience)}</div></div></section>
<section id="audio"><div class="shell"><div class="section-head"><div><div class="kicker">AUDIO IDENTITY</div><h2>Sound Archive</h2></div><p>Existing music, ambience, footsteps, alarms and voice experiments are included here as part of the production reference.</p></div><div class="grid" style="margin-bottom:28px">{cards(audio)}</div><div class="audio-grid">{''.join(audio_cards)}</div></div></section>
<section id="visuals"><div class="shell"><div class="section-head"><div><div class="kicker">CONCEPT / 3D</div><h2>Visual Archive</h2></div><p>All current visual references supplied in the Drive are browsable below.</p></div><div class="gallery-tools"><input id="gallerySearch" class="search" placeholder="Search visual assets…" oninput="filterGallery()"><button class="filter-btn active" data-filter="all" onclick="setGalleryFilter('all')">All</button><button class="filter-btn" data-filter="Concept Art" onclick="setGalleryFilter('Concept Art')">Concept Art</button><button class="filter-btn" data-filter="Model 3D" onclick="setGalleryFilter('Model 3D')">3D</button></div><div id="gallery" class="gallery">{''.join(img_cards)}</div></div></section>
<section id="docs"><div class="shell"><div class="section-head"><div><div class="kicker">SOURCE MATERIAL</div><h2>Document Archive</h2></div><p>Every narrative / production document in the supplied Drive is preserved here and readable inside the site.</p></div><div class="doc-grid">{''.join(doc_cards)}</div></div></section>
<section id="vx13"><div class="shell"><div class="section-head"><div><div class="kicker">HAZARD</div><h2>V-X13</h2></div><p>{html.escape(hazard)}</p></div><div class="grid">{cards([('EARLY EXPOSURE','Subtle environmental contamination and small anomalies.'),('INCREASING EXPOSURE','Stronger purple contamination, impaired vision and breathing discomfort.'),('SEVERE EXPOSURE','Movement, perception and audiovisual stability begin to fail.'),('DESIGN ROLE','V-X13 is simultaneously lore, threat, visual motif and gameplay feedback system.')])}</div></div></section>
<section id="recruitment"><div class="shell"><div class="section-head"><div><div class="kicker">JOIN THE PROJECT</div><h2>Recruitment</h2></div><p>The project is expanding from an established narrative foundation into a complete playable production.</p></div><div class="grid">{cards(recruit)}</div><div class="cta" style="margin-top:22px"><div><h3>Build the complex with us.</h3><p>New contributors should preserve the project's industrial credibility, uncertainty, mechanical identity, atmosphere and continuity.</p></div><a class="btn" href="#docs">Review project documents</a></div></div></section>
</main>
<footer><div class="shell footerline"><span>VOITHOS — Project Archive / Recruitment Edition</span><span>Built from the supplied project Drive archive.</span></div></footer>
<div id="lightbox" class="modal" onclick="closeLightbox(event)"><button class="modal-close" onclick="closeLightbox(event)">CLOSE</button><div class="lightbox"><img id="lightboxImg" src="" alt=""><div id="lightboxCaption" class="modal-caption"></div></div></div>
<div id="docModal" class="doc-modal"><div class="doc-reader">{''.join(doc_modal)}</div></div>
<script>
let currentFilter='all';
function filterGallery(){{const q=document.getElementById('gallerySearch').value.toLowerCase();document.querySelectorAll('.gallery-card').forEach(c=>{{const ok=(currentFilter==='all'||c.dataset.folder===currentFilter)&&(c.dataset.name.toLowerCase().includes(q));c.style.display=ok?'block':'none'}})}}
function setGalleryFilter(f){{currentFilter=f;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active',b.dataset.filter===f));filterGallery()}}
function openLightbox(el){{event.stopPropagation();document.getElementById('lightboxImg').src=el.querySelector('img').src;document.getElementById('lightboxCaption').textContent=el.dataset.name;document.getElementById('lightbox').classList.add('show');document.body.classList.add('no-scroll')}}
function closeLightbox(e){{if(e)e.stopPropagation();document.getElementById('lightbox').classList.remove('show');document.body.classList.remove('no-scroll')}}
function openDoc(id){{document.querySelectorAll('.doc-modal-content').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.getElementById('docModal').classList.add('show');document.body.classList.add('no-scroll');window.scrollTo(0,0)}}
function closeDoc(){{document.getElementById('docModal').classList.remove('show');document.body.classList.remove('no-scroll')}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape'){{closeLightbox();closeDoc()}}}});
</script>
</body></html>'''
(root/'index.html').write_text(page,encoding='utf-8')
print('site written',len(page),'chars')
