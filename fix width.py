from pathlib import Path
import re

HTML_FILE = "templates/settings.html"  # change if needed

html_path = Path(HTML_FILE)

if not html_path.exists():
    print(f"File not found: {HTML_FILE}")
    exit()

content = html_path.read_text(encoding="utf-8")

# Ensure Session card is mobile-only
content = content.replace(
    '<div class="card">\n\n        <h2>\n            Session',
    '<div class="card pwa-mobile-only">\n\n        <h2>\n            Session'
)

# Inject CSS block if not already present
css_block = """
<style>
/* Force settings cards to stack */
.settings-grid{
    display:flex !important;
    flex-direction:column !important;
    gap:20px !important;
}

/* Hide mobile-only items on desktop */
.pwa-mobile-only{
    display:none;
}

/* Show on mobile */
@media (max-width:768px){
    .pwa-mobile-only{
        display:block;
    }
}
</style>
"""

if ".pwa-mobile-only" not in content:
    content = css_block + "\n" + content

html_path.write_text(content, encoding="utf-8")

print("✓ settings.html updated successfully")