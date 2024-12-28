const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

document.getElementById("signup-toggle").addEventListener("click", () => {
    const passwordField = document.getElementById("signup-password");
    togglePassword(passwordField, "signup-toggle");
});

document.getElementById("signin-toggle").addEventListener("click", () => {
    const passwordField = document.getElementById("signin-password");
    togglePassword(passwordField, "signin-toggle");
});

// Toggle Function
function togglePassword(inputField, toggleIconId) {
    const icon = document.getElementById(toggleIconId);
    if (inputField.type === "password") {
        inputField.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        inputField.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

setTimeout(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        message.style.display = 'none';
    });
}, 5000);