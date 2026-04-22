    const deleteLinks = document.querySelectorAll(".delete-confirm");
    deleteLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const message = link.dataset.message || "Are you sure?";
            const confirmed = confirm(message);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
