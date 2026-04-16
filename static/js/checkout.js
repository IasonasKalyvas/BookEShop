document.addEventListener("DOMContentLoaded", () => {

    // ================= ELEMENTS =================
    const form = document.getElementById("checkoutForm");
    const popup = document.getElementById("popup");

    const nameInput = document.getElementById("name");
    const phoneInput = document.getElementById("phone");

    const addressSearch = document.getElementById("addressSearch");
    const addressResults = document.getElementById("addressResults");
    const addressInput = document.getElementById("addressInput");

    const cardNameInput = document.getElementById("cardName");
    const cardNumberInput = document.getElementById("cardNumber");
    const expiryInput = document.getElementById("expiry");
    const cvvInput = document.getElementById("cvv");

    if (!form || !popup) return;

    let selectedAddress = "";
    let submitTimer = null;
    let searchTimer = null;

    // ================= ERROR HANDLING =================
    function setError(input, message) {
        const group = input.parentElement;
        const error = group.querySelector(".error-msg");

        group.classList.add("invalid");
        if (error) {
            error.innerText = message;
            error.style.display = "block";
        }
    }

    function clearError(input) {
        const group = input.parentElement;
        const error = group.querySelector(".error-msg");

        group.classList.remove("invalid");
        if (error) error.style.display = "none";
    }

    // ================= AUTOCOMPLETE =================
    addressSearch.addEventListener("input", () => {

        selectedAddress = "";
        addressInput.value = "";

        clearTimeout(searchTimer);

        searchTimer = setTimeout(async () => {
            const q = addressSearch.value.trim();

            if (q.length < 3) {
                addressResults.innerHTML = "";
                return;
            }

            try {
                const res = await fetch(
                    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}`
                );

                const data = await res.json();
                addressResults.innerHTML = "";

                data.slice(0, 5).forEach(place => {
                    const div = document.createElement("div");
                    div.textContent = place.display_name;

                    div.addEventListener("click", () => {
                        addressSearch.value = place.display_name;
                        addressInput.value = place.display_name;
                        selectedAddress = place.display_name;
                        addressResults.innerHTML = "";
                    });

                    addressResults.appendChild(div);
                });

            } catch {
                console.log("Address API failed");
            }

        }, 400);
    });

    // ================= CARD FORMAT =================
    cardNumberInput.addEventListener("input", (e) => {
        let v = e.target.value.replace(/\D/g, "").slice(0, 16);
        e.target.value = v.match(/.{1,4}/g)?.join("-") || v;
    });

    expiryInput.addEventListener("input", (e) => {
        let v = e.target.value.replace(/\D/g, "").slice(0, 4);
        e.target.value = v.length > 2 ? v.slice(0, 2) + "/" + v.slice(2) : v;
    });

    // ================= VALIDATION =================
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        let valid = true;

        // NAME
        if (!/^[A-Za-z\s]+$/.test(nameInput.value.trim())) {
            setError(nameInput, "Only letters allowed");
            valid = false;
        } else clearError(nameInput);

        // PHONE
        if (!/^\d{10}$/.test(phoneInput.value.trim())) {
            setError(phoneInput, "Must be 10 digits");
            valid = false;
        } else clearError(phoneInput);

        // CARD NAME
        if (!/^[A-Za-z\s]+$/.test(cardNameInput.value.trim())) {
            setError(cardNameInput, "Only letters allowed");
            valid = false;
        } else clearError(cardNameInput);

        // CARD NUMBER
        if (cardNumberInput.value.replace(/\D/g, "").length !== 16) {
            setError(cardNumberInput, "Must be 16 digits");
            valid = false;
        } else clearError(cardNumberInput);

        // CVV
        if (!/^\d{3}$/.test(cvvInput.value.trim())) {
            setError(cvvInput, "Must be 3 digits");
            valid = false;
        } else clearError(cvvInput);

        // ADDRESS
        if (!selectedAddress) {
            setError(addressSearch, "Please select an address");
            valid = false;
        } else clearError(addressSearch);

        // EXPIRY
        const match = expiryInput.value.match(/^(\d{2})\/(\d{2})$/);

        if (!match) {
            setError(expiryInput, "Use MM/YY format");
            valid = false;
        } else {
            const month = +match[1];
            const year = +match[2];

            const now = new Date();
            const cy = now.getFullYear() % 100;
            const cm = now.getMonth() + 1;

            if (month < 1 || month > 12 || year < cy || (year === cy && month < cm)) {
                setError(expiryInput, "Invalid expiry date");
                valid = false;
            } else {
                clearError(expiryInput);
            }
        }

        if (!valid) return;

        // ================= POPUP =================
        popup.style.display = "flex";

        submitTimer = setTimeout(() => {
            form.submit();
        }, 5000);
    });

    // ================= POPUP BUTTON =================
    const popupLink = document.querySelector("#popup a");

    if (popupLink) {
        popupLink.addEventListener("click", (e) => {
            e.preventDefault();
            if (submitTimer) clearTimeout(submitTimer);
            form.submit();
        });
    }
});