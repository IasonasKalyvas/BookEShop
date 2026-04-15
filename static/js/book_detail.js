document.addEventListener("DOMContentLoaded", function () {

    const gallery = document.querySelector(".book-gallery");
    if (!gallery) return;

    const images = gallery.dataset.images
        ? gallery.dataset.images.split(",")
        : [];

    if (!images.length) return;

    let currentIndex = 0;

    const mainImage = document.getElementById("mainImage");
    const prevBtn = document.querySelector(".carousel-prev");
    const nextBtn = document.querySelector(".carousel-next");
    const thumbnails = document.querySelectorAll(".thumbnail");

    function updateImage() {
        mainImage.src = images[currentIndex];

        thumbnails.forEach((thumb, index) => {
            thumb.classList.toggle("active", index === currentIndex);
        });
    }

    if (prevBtn && nextBtn) {
        prevBtn.addEventListener("click", () => {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            updateImage();
        });

        nextBtn.addEventListener("click", () => {
            currentIndex = (currentIndex + 1) % images.length;
            updateImage();
        });
    }

    thumbnails.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            currentIndex = parseInt(thumb.dataset.index);
            updateImage();
        });
    });

});

document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".read-more-btn");

    buttons.forEach(btn => {
        const targetId = btn.dataset.target;
        const text = document.getElementById(targetId);

        if (!text) return;

        // STEP 1: measure full height
        text.classList.remove("collapsed");
        text.classList.add("expanded");

        const fullHeight = text.scrollHeight;

        // STEP 2: apply collapsed and measure again
        text.classList.remove("expanded");
        text.classList.add("collapsed");

        const collapsedHeight = text.clientHeight;

        // STEP 3: compare
        if (fullHeight <= collapsedHeight + 2) {
            // ❌ Text is SHORT → no button
            btn.style.display = "none";
            text.classList.remove("collapsed");
            return;
        }

        // ✅ Text is LONG → enable button
        btn.style.display = "inline-block";

        btn.addEventListener("click", () => {
            const isCollapsed = text.classList.contains("collapsed");

            if (isCollapsed) {
                text.classList.remove("collapsed");
                text.classList.add("expanded");
                btn.textContent = "Read less";
            } else {
                text.classList.add("collapsed");
                text.classList.remove("expanded");
                btn.textContent = "Read more";
            }
        });
    });
});