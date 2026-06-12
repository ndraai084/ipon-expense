from pathlib import Path

file = Path("static/css/modern.css")

text = file.read_text(encoding="utf-8")

if "MOBILE SIDEBAR COMPACT" not in text:

    text += """

/* =====================================
   MOBILE SIDEBAR COMPACT
   ===================================== */

@media (max-width:768px){

    .sidebar{

        height:100vh !important;

        display:flex !important;
        flex-direction:column;

        overflow:hidden;
    }

    .sidebar-header{

        padding:16px 20px !important;
    }

    .sidebar-header h2{

        font-size:1.5rem !important;
        margin:0 !important;
    }

    .sidebar-links{

        flex:1;

        overflow-y:auto;

        padding:8px 0;
    }

    .sidebar-links a{

        padding:12px 20px !important;
        font-size:1rem !important;
    }

    .sidebar-footer{

        flex-shrink:0;

        border-top:1px solid rgba(255,255,255,.15);

        padding:12px 20px !important;
    }

    .sidebar-footer a{

        font-size:1rem !important;
    }

}
"""

    file.write_text(text, encoding="utf-8")

    print("Mobile sidebar compact mode added.")

else:

    print("Patch already exists.")