
document.addEventListener(
'DOMContentLoaded',
() => {

    const burger =
        document.getElementById(
            'burger-btn'
        );

    const sidebar =
        document.getElementById(
            'sidebar'
        );

    const overlay =
        document.getElementById(
            'overlay'
        );

    // only show burger if sidebar exists
    if(sidebar){
        document.body.classList.add(
            'logged-in'
        );
    }

    if(
        !burger ||
        !sidebar ||
        !overlay
    ){
        return;
    }

    burger.addEventListener(
        'click',
        () => {

            sidebar.classList.toggle(
                'active'
            );

            overlay.classList.toggle(
                'active'
            );

        }
    );

    overlay.addEventListener(
        'click',
        () => {

            sidebar.classList.remove(
                'active'
            );

            overlay.classList.remove(
                'active'
            );

        }
    );

});