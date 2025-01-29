const popup = document.getElementById('signup-popup');
const openPopup = document.getElementById('open-popup');
const closePopup = document.getElementById('close-popup');

// Show the popup
openPopup.addEventListener('click', () => {
    popup.style.display = 'flex';
});

// Close the popup
closePopup.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Close the popup when clicking outside the content
window.addEventListener('click', (e) => {
    if (e.target === popup) {
        popup.style.display = 'none';
    }
});