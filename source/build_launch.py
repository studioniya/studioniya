"""Build the public site into ../launch from template.html + works.js + img/.
Run: python3 build_launch.py   (the preview build is index.html; this one drops the preview bar and adds proper page metadata)."""
import os, re, shutil, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "launch")
DOMAIN = "studioniya.com"

tpl = open(os.path.join(HERE, "template.html")).read()
works = open(os.path.join(HERE, "works.js")).read()
html = tpl.replace("/*WORKS*/", works)

# Drop the preview-only bar and the artifact-only meta tag.
html = html.replace('<div class="preview"><div class="gut">Private preview · not live yet</div></div>\n', "")
html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
assert "Private preview" not in html

# Favicon: the charcoal stub used as the cursor.
stub = re.search(r'cursor: url\("(data:image/svg\+xml,[^"]+)"\)', html).group(1)

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Niya Prabhakar is a London-based artist working across painting, installation and spatial storytelling.">
<meta property="og:title" content="Niya Prabhakar">
<meta property="og:description" content="Painting, installation and spatial storytelling. London.">
<meta property="og:image" content="https://{DOMAIN}/img/the-fabric-of-persistence-main-1.jpg">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://{DOMAIN}/">
<link rel="icon" href="{stub}">
"""
html = head + html.replace("<title>Niya Prabhakar</title>\n", "<title>Niya Prabhakar</title>\n</head>\n<body>\n", 1) + "\n</body>\n</html>\n"

# Copy only the images the site actually uses.
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "img"))
used = set(re.findall(r'[\w.-]+\.(?:jpg|png|mp4)', html))
for f in os.listdir(os.path.join(HERE, "img")):
    if f in used or f.replace("-t.jpg", ".jpg") in used or f.startswith("daana-pani-book-"):
        shutil.copy2(os.path.join(HERE, "img", f), os.path.join(OUT, "img", f))
open(os.path.join(OUT, "index.html"), "w").write(html)
open(os.path.join(OUT, "CNAME"), "w").write(DOMAIN + "\n")
print("built", OUT, len(os.listdir(os.path.join(OUT, "img"))), "images")
