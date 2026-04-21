console.log("Website loaded successfully");

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM is ready");

    // ================= ADD TO CART BUTTONS =================
    const buttons = document.getElementsByClassName("add-to-cart");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function () {
            alert("Book added to cart!");
        });
    }

    // ================= DARK MODE TOGGLE =================
    const darkModeToggle = document.getElementById("darkModeToggle");

    console.log("Dark mode button:", darkModeToggle);

    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", function () {
            console.log("🔥 DARK MODE CLICKED");

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {
                darkModeToggle.textContent = "☀️";
            } else {
                darkModeToggle.textContent = "🌙";
            }
        });
    }
});