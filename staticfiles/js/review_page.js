document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.querySelector("textarea");
    const counter = document.getElementById("charCount");
    // Character counter for review textarea, updating live as the user types and enforcing a maximum of 50 characters
    if (textarea && counter) {
        textarea.addEventListener("input", function () {
            const length = textarea.value.length;

            counter.textContent = `${length} / 50`;
            if (length > 50) {
                textarea.value = textarea.value.substring(0, 50);
            }
        });
    }
});