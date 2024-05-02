document.addEventListener("DOMContentLoaded", function() {
    let logoutButton = document.querySelector(".dropdown-item-logout");
    let logoutLink = document.querySelector(".dropdown-item-logout-link");

    logoutButton.addEventListener("click", function(event) {

        event.preventDefault();

        event.stopPropagation();

        logoutLink.style.display = (logoutLink.style.display === "none" || logoutLink.style.display === "") ? "block" : "none";
    });
});