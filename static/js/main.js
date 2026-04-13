/* Will probably delete all this in the future */

console.log("Website loaded successfully");

/* Example: simple click message */
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM is ready");
    const buttons = document.querySelectorAll(".add-to-cart");
    buttons.forEach(btn => {
        btn.addEventListener("click", function () {
            alert("Book added to cart!");
        });
    });

});