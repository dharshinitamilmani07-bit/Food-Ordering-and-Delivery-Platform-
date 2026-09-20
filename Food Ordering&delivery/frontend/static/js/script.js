document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide flash messages
    setTimeout(function () {

        const messages =
            document.querySelectorAll(".flash");

        messages.forEach(function (message) {
            message.style.opacity = "0";

            setTimeout(function () {
                message.remove();
            }, 500);
        });

    }, 3000);


    // Confirm remove actions
    const removeLinks =
        document.querySelectorAll(
            ".subtotal a"
        );

    removeLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const result = confirm(
                    "Remove this item from cart?"
                );

                if (!result) {
                    event.preventDefault();
                }

            }
        );

    });

});