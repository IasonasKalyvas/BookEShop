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
        if (!images.length) return;
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

const reviewCarousel = document.querySelector(".reviews-wrapper");
const reviewSlides = document.querySelectorAll(".review-slide");
const reviewPrev = document.querySelector(".review-prev");
const reviewNext = document.querySelector(".review-next");

if (reviewCarousel && reviewSlides.length > 0) {
    let reviewIndex = 0;

    function updateReviews() {
        const containerWidth = reviewCarousel.parentElement.offsetWidth;
        reviewSlides.forEach(slide => {
            slide.style.minWidth = containerWidth + "px";
        });
        reviewCarousel.style.transform = `translateX(-${reviewIndex * containerWidth}px)`;
    }

    reviewNext?.addEventListener("click", () => {
        reviewIndex = (reviewIndex + 1) % reviewSlides.length;
        updateReviews();
    });

    reviewPrev?.addEventListener("click", () => {
        reviewIndex = (reviewIndex - 1 + reviewSlides.length) % reviewSlides.length;
        updateReviews();
    });

    updateReviews();
    window.addEventListener("resize", updateReviews);
}

const wishlistBtn = document.getElementById("wishlistBtn");
const wishlistPopup = document.getElementById("wishlistPopup");

function showPopup(message) {
    if (!wishlistPopup) return;
    wishlistPopup.textContent = message;
    wishlistPopup.classList.add("show");
    setTimeout(() => {
        wishlistPopup.classList.remove("show");
    }, 2000);
}

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

if (wishlistBtn) {
    wishlistBtn.addEventListener("click", function () {
        const bookId = this.dataset.bookId;
        const csrftoken = getCookie("csrftoken");

        fetch(`/accounts/wishlist/toggle/${bookId}/`, {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken }
        })
        .then(res => res.json())
        .then(data => {
            this.innerHTML = data.status === "added" ? "💖" : "🤍";
            showPopup(
                data.status === "added"
                    ? "Book added to wishlist"
                    : "Book removed from wishlist"
            );
        })
        .catch(() => {
            showPopup("Something went wrong");
        });
    });
}