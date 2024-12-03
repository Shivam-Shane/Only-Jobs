document.addEventListener("DOMContentLoaded", function() {
    // Select the messages container
    const messages = document.getElementById("messages");
    if (messages) {
        // Set a timeout to fade out and remove the messages
        setTimeout(function() {
            messages.style.transition = "opacity 0.5s ease";
            messages.style.opacity = "0";
            setTimeout(() => messages.remove(), 500); // Remove after fade out
        }, 2000); // Adjust time in milliseconds (3000 = 3 seconds)
    }
});
