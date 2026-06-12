from pathlib import Path

file = Path("static/css/modern.css")

text = file.read_text(encoding="utf-8")

if "EDIT MODAL WHITE THEME" not in text:

    text += """

/* =====================================
   EDIT MODAL WHITE THEME
   ===================================== */

.modal,
.edit-modal,
.modal-content{

    background:#FFFFFF !important;
    color:#111827 !important;
}

.modal h2,
.modal h3,
.modal label,
.modal p,
.edit-modal h2,
.edit-modal h3,
.edit-modal label,
.edit-modal p{

    color:#111827 !important;
}

.modal input,
.modal select,
.modal textarea,
.edit-modal input,
.edit-modal select,
.edit-modal textarea{

    background:#FFFFFF !important;
    color:#111827 !important;
    border:1px solid #D1D5DB;
}

/* =====================================
   DROPDOWN PADDING FIX
   ===================================== */

select{

    padding-right:2.75rem !important;

    appearance:none;
    -webkit-appearance:none;
    -moz-appearance:none;

    background-position:
        right 14px center !important;

    background-repeat:no-repeat;
}

"""

    file.write_text(
        text,
        encoding="utf-8"
    )

    print("Modal and dropdown patch added.")

else:

    print("Patch already exists.")