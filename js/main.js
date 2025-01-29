let index = 0;
      function moveSlide(step) {
        const sliderWrapper = document.querySelector(".slider-wrapper");
        const totalSlides = document.querySelectorAll(
          ".expert-box .profile"
        ).length;
        const slideWidth = document.querySelector(".profile").offsetWidth;
        const visibleSlides = 1;
        const maxIndex = totalSlides - visibleSlides;

        index += step;
        if (index > maxIndex) {
          index = 0;
        } else if (index < 0) {
          index = maxIndex;
        }

        sliderWrapper.style.transform = `translateX(${-index * slideWidth}px)`;
      }

// Global Event Listeners and Navigation

// Show Feedback option after login
document.addEventListener("DOMContentLoaded", () => {
  // Handle login functionality
  document.querySelector("#login-form button").addEventListener("click", handleLogin);
  
  // Handle logout functionality
  document.querySelector("#logout-nav a").addEventListener("click", logout);
  
  // Show menu links on burger click
  $("#menu-btn").click(() => $("nav .navigation ul").addClass("active"));
  
  // Hide navbar on click
  $("#menu-close").click(() => $("nav .navigation ul").removeClass("active"));
  
  // Toggle Read More / Read Less functionality
  document.querySelectorAll(".read-more-btn").forEach(button => {
    button.addEventListener("click", toggleReadMore);
  });
});

// Handle login functionality
function handleLogin() {
  const username = document.querySelector("#login-form input[type='text']").value;
  const password = document.querySelector("#login-form input[type='password']").value;

  if (username && password) {
    alert(`Logged in successfully!\nUsername: ${username}`);
    
    // Show the Feedback menu item
    document.getElementById("feedback-nav").classList.remove("hidden");
    
    // Show Logout and hide Signup
    document.getElementById("signup-nav").classList.add("hidden");
    document.getElementById("logout-nav").classList.remove("hidden");
    
    // Close the popup after successful login
    closePopup();
  } else {
    alert("Please enter both username and password to log in.");
  }
}


// Logout functionality
function logout() {
  alert("You have logged out successfully!");

  // Hide Feedback and Logout
  document.getElementById("feedback-nav").classList.add("hidden");
  document.getElementById("logout-nav").classList.add("hidden");

  // Show Signup
  document.getElementById("signup-nav").classList.remove("hidden");

  closePopup(); // Optionally close any open popups
}

// Toggle Read More / Read Less functionality
function toggleReadMore(event) {
  const fullContent = event.target.previousElementSibling;
  if (fullContent.style.display === "block") {
    fullContent.style.display = "none";
    event.target.textContent = "Read More";
  } else {
    fullContent.style.display = "block";
    event.target.textContent = "Read Less";
  }
}

// Popup and Form Management

// Function to show the popup
function openPopup() {
  document.getElementById("signup-popup").classList.remove("hidden");
}

// Function to close the popup
function closePopup() {
  document.getElementById("signup-popup").classList.add("hidden");
}

// Function to toggle between different forms in the popup
function showForm(formId) {
  const forms = document.querySelectorAll(".form-container");
  forms.forEach((form) => (form.style.display = "none"));
  document.getElementById(formId).style.display = "block";
}
// Register Form Validation

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#register-form button").addEventListener("click", handleRegister);
  
  // Handle Google Login Button Click
  document.querySelector(".google-btn").addEventListener("click", () => {
    alert("Google login simulated! Redirecting to Google login page...");
  });
});

// Handle Register Button Click
function handleRegister() {
  const fullName = document.querySelector("#register-form input[type='text']").value;
  const email = document.querySelector("#register-form input[type='email']").value;
  const password = document.querySelector("#register-form input[type='password']").value;

  // Validate Email
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Validate Password (at least 8 characters and alphanumeric)
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
  if (!passwordRegex.test(password)) {
    alert("Password must be at least 8 characters long and contain both letters and numbers.");
    return;
  }

  if (fullName && email && password) {
    alert(`Registered successfully!\nName: ${fullName}\nEmail: ${email}`);
    showForm("login-form"); // Redirect to login form after registration
  } else {
    alert("Please fill in all fields to register.");
  }
}

// Forgot Password

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#forgot-password-form button").addEventListener("click", handleForgotPassword);
});

// Handle Forgot Password functionality
function handleForgotPassword() {
  const email = document.querySelector("#forgot-password-form input[type='email']").value;

  // Validate Email for forgot password
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Simulate sending the reset link
  alert(`Reset link sent to: ${email}`);
  showForm("login-form"); // Redirect to login form after reset link
}
