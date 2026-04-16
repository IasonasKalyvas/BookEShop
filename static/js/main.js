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

    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
        });
    }
});