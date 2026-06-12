from pathlib import Path

file = Path("templates/dashboard.html")

text = file.read_text(
    encoding="utf-8"
)

if "AUTO DATE TIME FILL" not in text:

    patch = """

<script>

/* AUTO DATE TIME FILL */

document.addEventListener(
'DOMContentLoaded',
() => {

    const dateField =
        document.querySelector(
            'input[name="date"]'
        );

    const timeField =
        document.querySelector(
            'input[name="time"]'
        );

    const now = new Date();

    if(dateField){

        dateField.value =
            now.toISOString()
                .split('T')[0];
    }

    if(timeField){

        const hours =
            String(
                now.getHours()
            ).padStart(2,'0');

        const minutes =
            String(
                now.getMinutes()
            ).padStart(2,'0');

        timeField.value =
            `${hours}:${minutes}`;
    }

});

</script>

"""

    text = text.replace(
        "{% endblock %}",
        patch + "\n{% endblock %}"
    )

    file.write_text(
        text,
        encoding="utf-8"
    )

    print("Patched dashboard.html")

else:

    print("Already patched.")