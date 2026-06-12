from pathlib import Path

file = Path("static/css/modern.css")

text = file.read_text(encoding="utf-8")

patch = """

/* =====================================
   MOBILE TABLE FIX
   ===================================== */

@media (max-width:768px){

    .card table{
        display:table !important;
        width:100%;
        min-width:600px;
    }

    .card{
        overflow-x:auto;
    }

}
"""

if "MOBILE TABLE FIX" not in text:
    text += patch
    file.write_text(text, encoding="utf-8")
    print("Added mobile table fix.")
else:
    print("Fix already exists.")

print("Done.")