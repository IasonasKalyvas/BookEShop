document.addEventListener("DOMContentLoaded", () => {

    // ================= GALLERY =================
    const gallery = document.getElementById("book-gallery");
    const mainImage = document.getElementById("mainImage");
    const prevBtn = document.getElementById("carouselPrev");
    const nextBtn = document.getElementById("carouselNext");

    const thumbnails = document.querySelectorAll(".thumbnail");

    let images = [];
    let currentIndex = 0;

    if (gallery && mainImage) {
        images = gallery.dataset.images
            ? gallery.dataset.images.split(",")
            : [];

        function updateImage() {
            mainImage.src = images[currentIndex];

            thumbnails.forEach((thumb, i) => {
                thumb.classList.toggle("active", i === currentIndex);
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                updateImage();
            });
        }

        if (nextBtn) {
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
    }

    // ================= QUANTITY =================
    const qtyInput = document.getElementById("qty");
    const plusBtn = document.getElementById("qtyPlus");
    const minusBtn = document.getElementById("qtyMinus");

    if (!qtyInput) return;

    const maxStock = parseInt(qtyInput.max) || 1;

    if (plusBtn) {
        plusBtn.addEventListener("click", () => {
            let value = parseInt(qtyInput.value) || 1;
            if (value < maxStock) qtyInput.value = value + 1;
        });
    }

    if (minusBtn) {
        minusBtn.addEventListener("click", () => {
            let value = parseInt(qtyInput.value) || 1;
            if (value > 1) qtyInput.value = value - 1;
        });
    }

    qtyInput.addEventListener("input", () => {
        let value = parseInt(qtyInput.value) || 1;

        if (value > maxStock) qtyInput.value = maxStock;
        if (value < 1) qtyInput.value = 1;
    });

});