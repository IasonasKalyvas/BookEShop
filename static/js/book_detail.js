// Image carousel functionality
const gallery = document.getElementById("book-gallery");
const mainImage = document.getElementById("mainImage");
const prevBtn = document.getElementById("carouselPrev");
const nextBtn = document.getElementById("carouselNext");
const thumbnails = document.querySelectorAll(".thumbnail");

let images = [];
let currentIndex = 0;

// Initialize image gallery if elements exist
if (gallery && mainImage) {
    images = gallery.dataset.images ? gallery.dataset.images.split(",") : [];

    // Update main image and active thumbnail
    function updateImage() {
        if (!images.length) return;
        mainImage.src = images[currentIndex];
        thumbnails.forEach((t, i) => t.classList.toggle("active", i === currentIndex));
    }

    // Navigate to previous image
    prevBtn?.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateImage();
    });

    // Navigate to next image
    nextBtn?.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateImage();
    });

    // Thumbnail click navigation
    thumbnails.forEach((t) => {
        t.addEventListener("click", () => {
            currentIndex = parseInt(t.dataset.index);
            updateImage();
        });
    });
}

// Quantity selector functionality
const qtyInput = document.getElementById("qty");
const plusBtn = document.getElementById("qtyPlus");
const minusBtn = document.getElementById("qtyMinus");

if (qtyInput) {
    const maxStock = parseInt(qtyInput.max) || 1;

    // Increase quantity (respects stock limit)
    plusBtn?.addEventListener("click", () => {
        let v = parseInt(qtyInput.value) || 1;
        if (v < maxStock) qtyInput.value = v + 1;
    });

    // Decrease quantity (minimum 1)
    minusBtn?.addEventListener("click", () => {
        let v = parseInt(qtyInput.value) || 1;
        if (v > 1) qtyInput.value = v - 1;
    });
}

// Review carousel functionality
const reviewCarousel = document.querySelector(".reviews-wrapper");
const reviewSlides = document.querySelectorAll(".review-slide");
const reviewPrev = document.querySelector(".review-prev");
const reviewNext = document.querySelector(".review-next");

if (reviewCarousel && reviewSlides.length > 0) {
    let reviewIndex = 0;

    // Update visible review slide
    function updateReviews() {
        const width = reviewSlides[0].offsetWidth;
        reviewCarousel.style.transform = `translateX(-${reviewIndex * width}px)`;
    }

    // Next review
    reviewNext?.addEventListener("click", () => {
        reviewIndex = (reviewIndex + 1) % reviewSlides.length;
        updateReviews();
    });

    // Previous review
    reviewPrev?.addEventListener("click", () => {
        reviewIndex = (reviewIndex - 1 + reviewSlides.length) % reviewSlides.length;
        updateReviews();
    });

    window.addEventListener("resize", updateReviews);
}

// Wishlist toggle functionality
const wishlistBtn = document.getElementById("wishlistBtn");
const wishlistPopup = document.getElementById("wishlistPopup");

// Show temporary popup message
function showPopup(message) {
    if (!wishlistPopup) return;
    wishlistPopup.textContent = message;
    wishlistPopup.classList.add("show");
    setTimeout(() => {
        wishlistPopup.classList.remove("show");
    }, 2000);
}

// Get CSRF token from cookies
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

// Handle wishlist toggle request
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