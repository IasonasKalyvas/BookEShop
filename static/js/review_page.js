document.addEventListener("DOMContentLoaded", function () {

    const textarea = document.querySelector("textarea");
    const counter = document.getElementById("charCount");

    if (textarea && counter) {
        textarea.addEventListener("input", function () {
            const length = textarea.value.length;
            counter.textContent = `${length} / 300`;

            if (length > 300) {
                textarea.value = textarea.value.substring(0, 300);
            }
        });
    }

});