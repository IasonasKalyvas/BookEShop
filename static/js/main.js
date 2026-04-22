document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.getElementsByClassName("add-to-cart");

    // Attach click event to all add-to-cart buttons
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function () {
            alert("Book added to cart!");
        });
    }

    // Dark mode toggle button
    const darkModeToggle = document.getElementById("darkModeToggle");

    // Load saved dark mode preference from localStorage
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        if (darkModeToggle) {
            darkModeToggle.textContent = "☀️";
        }
    }
    // Toggle dark mode on click
    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
            // Save preference and update icon
            if (document.body.classList.contains("dark-mode")) {
                darkModeToggle.textContent = "☀️";
                localStorage.setItem("darkMode", "enabled");
            } else {
                darkModeToggle.textContent = "🌙";
                localStorage.setItem("darkMode", "disabled");
            }
        });
    }
});