document.addEventListener("DOMContentLoaded", () => {

    // ================= IMAGE CAROUSEL =================
    const gallery = document.getElementById("book-gallery");
    const mainImage = document.getElementById("mainImage");
    const prevBtn = document.getElementById("carouselPrev");
    const nextBtn = document.getElementById("carouselNext");
    const thumbnails = document.querySelectorAll(".thumbnail");

    let images = [];
    let currentIndex = 0;

    if (gallery && mainImage) {
        images = gallery.dataset.images ? gallery.dataset.images.split(",") : [];

        function updateImage() {
            mainImage.src = images[currentIndex];
            thumbnails.forEach((t, i) => t.classList.toggle("active", i === currentIndex));
        }

        prevBtn?.addEventListener("click", () => {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            updateImage();
        });

        nextBtn?.addEventListener("click", () => {
            currentIndex = (currentIndex + 1) % images.length;
            updateImage();
        });

        thumbnails.forEach((t) => {
            t.addEventListener("click", () => {
                currentIndex = parseInt(t.dataset.index);
                updateImage();
            });
        });
    }

    // ================= QUANTITY =================
    const qtyInput = document.getElementById("qty");
    const plusBtn = document.getElementById("qtyPlus");
    const minusBtn = document.getElementById("qtyMinus");

    if (qtyInput) {
        const maxStock = parseInt(qtyInput.max) || 1;

        plusBtn?.addEventListener("click", () => {
            let v = parseInt(qtyInput.value) || 1;
            if (v < maxStock) qtyInput.value = v + 1;
        });

        minusBtn?.addEventListener("click", () => {
            let v = parseInt(qtyInput.value) || 1;
            if (v > 1) qtyInput.value = v - 1;
        });
    }

    // ================= REVIEW CAROUSEL (FIXED WORKING) =================
    const reviewCarousel = document.querySelector(".reviews-wrapper");
    const reviewSlides = document.querySelectorAll(".review-slide");
    const reviewPrev = document.querySelector(".review-prev");
    const reviewNext = document.querySelector(".review-next");

    if (reviewCarousel && reviewSlides.length > 0) {
        let index = 0;

        function updateReviews() {
            const width = reviewCarousel.clientWidth;
            reviewCarousel.style.transform = `translateX(-${index * width}px)`;
        }

        reviewNext?.addEventListener("click", () => {
            index = (index + 1) % reviewSlides.length;
            updateReviews();
        });

        reviewPrev?.addEventListener("click", () => {
            index = (index - 1 + reviewSlides.length) % reviewSlides.length;
            updateReviews();
        });

        window.addEventListener("resize", updateReviews);
    }

// ================= WISHLIST =================
const wishlistBtn = document.getElementById("wishlistBtn");
const wishlistPopup = document.getElementById("wishlistPopup");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// 🔥 SHOW POPUP FUNCTION
function showPopup(message) {
    if (!wishlistPopup) return;

    wishlistPopup.textContent = message;
    wishlistPopup.classList.add("show");

    setTimeout(() => {
        wishlistPopup.classList.remove("show");
    }, 2000);
}

if (wishlistBtn) {
    wishlistBtn.addEventListener("click", function () {

        const bookId = wishlistBtn.getAttribute("data-book-id");

        fetch(`/accounts/wishlist/toggle/${bookId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            }
        })
        .then(res => res.json())
        .then(data => {

            if (data.status === "added") {
                wishlistBtn.textContent = "💖";
                showPopup("Book successfully added to wishlist");
            } else {
                wishlistBtn.textContent = "🤍";
                showPopup("Book successfully removed from wishlist");
            }

        })
        .catch(err => console.error(err));
    });
}


});

