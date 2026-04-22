document.addEventListener("DOMContentLoaded", function () {
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
    const popupLink = document.getElementById("popupLink");

    if (!form || !popup) return;
    let selectedAddress = "";
    let submitTimer = null;
    let searchTimer = null;

    // Function to set error state for an input field, displaying an error message and adding invalid styling to the input's parent element
    function setError(input, message) {
        const group = input.parentElement;
        const error = group.querySelector(".error-msg");

        group.classList.add("invalid");
        if (error) {
            error.innerText = message;
            error.style.display = "block";
        }
    }
    // Function to clear error state for an input field, hiding the error message and removing invalid styling from the input's parent element
    function clearError(input) {
        const group = input.parentElement;
        const error = group.querySelector(".error-msg");
        group.classList.remove("invalid");
        if (error) error.style.display = "none";
    }

    // Address autocomplete using OpenStreetMap API with debouncing to limit API calls, displaying results in a dropdown and allowing users to select an address which populates the hidden input for form submission
    addressSearch.addEventListener("input", function () {
        selectedAddress = "";
        addressInput.value = "";
        clearTimeout(searchTimer);
        searchTimer = setTimeout(async function () {
            const q = addressSearch.value.trim();

            if (q.length < 3) {
                addressResults.innerHTML = "";
                return;
            }
            try {
                const res = await fetch(
                    "https://nominatim.openstreetmap.org/search?format=json&q=" +
                    encodeURIComponent(q)
                );
                const data = await res.json();

                addressResults.innerHTML = "";
                data.slice(0, 5).forEach(function (place) {
                    const div = document.createElement("div");

                    div.textContent = place.display_name;
                    div.addEventListener("click", function () {
                        addressSearch.value = place.display_name;
                        addressInput.value = place.display_name;
                        selectedAddress = place.display_name;
                        addressResults.innerHTML = "";
                    });
                    addressResults.appendChild(div);
                });
            } catch (e) {
                console.log("Address API failed");
            }
        }, 400);
    });

    // Card number formatting (auto-insert dashes) and expiry date formatting (auto-insert slash)
    cardNumberInput.addEventListener("input", function (e) {
        let v = e.target.value.replace(/\D/g, "").slice(0, 16);
        e.target.value = v.match(/.{1,4}/g)?.join("-") || v;
    });
    expiryInput.addEventListener("input", function (e) {
        let v = e.target.value.replace(/\D/g, "").slice(0, 4);
        e.target.value = v.length > 2 ? v.slice(0, 2) + "/" + v.slice(2) : v;
    });

    // Form submission with validation and delayed submit for popup
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        let valid = true;
        if (!/^[A-Za-z\s]+$/.test(nameInput.value.trim())) {
            setError(nameInput, "Only letters allowed");
            valid = false;
        } else clearError(nameInput);
        if (!/^\d{10}$/.test(phoneInput.value.trim())) {
            setError(phoneInput, "Must be 10 digits");
            valid = false;
        } else clearError(phoneInput);
        if (!/^[A-Za-z\s]+$/.test(cardNameInput.value.trim())) {
            setError(cardNameInput, "Only letters allowed");
            valid = false;
        } else clearError(cardNameInput);
        if (cardNumberInput.value.replace(/\D/g, "").length !== 16) {
            setError(cardNumberInput, "Must be 16 digits");
            valid = false;
        } else clearError(cardNumberInput);
        if (!/^\d{3}$/.test(cvvInput.value.trim())) {
            setError(cvvInput, "Must be 3 digits");
            valid = false;
        } else clearError(cvvInput);
        if (!selectedAddress) {
            setError(addressSearch, "Please select an address");
            valid = false;
        } else clearError(addressSearch);
        const match = expiryInput.value.match(/^(\d{2})\/(\d{2})$/);

        if (!match) {
            setError(expiryInput, "Use MM/YY format");
            valid = false;
        } else {
            const month = parseInt(match[1]);
            const year = parseInt(match[2]);
            const now = new Date();
            const currentYear = now.getFullYear() % 100;
            const currentMonth = now.getMonth() + 1;

            if (month < 1 || month > 12 || year < currentYear ||
                (year === currentYear && month < currentMonth)) {
                setError(expiryInput, "Invalid expiry date");
                valid = false;
            } else {
                clearError(expiryInput);
            }
        }
        if (!valid) return;

        // Show popup and delay actual submission to allow user to see confirmation message, with option to submit immediately via popup button
        popup.style.display = "flex";
        submitTimer = setTimeout(function () {
            form.submit();
        }, 5000);
    });

    // Popup link allows user to bypass the 5 second delay and submit immediately if they choose, improving user experience for those who don't want to wait
    if (popupLink) {
        popupLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (submitTimer) clearTimeout(submitTimer);
            form.submit();
        });
    }
});