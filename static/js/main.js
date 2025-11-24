// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("HVAC Booking site loaded successfully!");

    // --- Booking Form Validation ---
    const bookingForm = document.querySelector("form[action='/book']");
    if (bookingForm) {
        bookingForm.addEventListener("submit", (e) => {
            const date = bookingForm.querySelector("input[name='date']").value;
            const time = bookingForm.querySelector("input[name='time']").value;

            if (!date || !time) {
                alert("Please choose both date and time for your service.");
                e.preventDefault();
            }
        });
    }

    // --- Password Visibility Toggle ---
    const passwordInputs = document.querySelectorAll("input[type='password']");
    passwordInputs.forEach(input => {
        const toggle = document.createElement("span");
        toggle.textContent = "👁️";
        toggle.style.cursor = "pointer";
        toggle.style.marginLeft = "10px";

        toggle.addEventListener("click", () => {
            input.type = input.type === "password" ? "text" : "password";
        });

        input.parentNode.insertBefore(toggle, input.nextSibling);
    });

    // --- Flash Message Auto-Dismiss ---
    const flashMessages = document.querySelectorAll("ul li");
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => msg.remove());
        }, 4000);
    }
});
