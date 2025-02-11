// Get the pop-up and the button to open it
const openPopupBtn = document.getElementById('openPopupBtn');
const popup = document.getElementById('popup');
const closeBtn = document.getElementById('closeBtn');

// Open the pop-up when the button is clicked
openPopupBtn.addEventListener('click', () => {
    popup.style.display = 'block';
});

// Close the pop-up when the close button is clicked
closeBtn.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Close the pop-up if the user clicks outside of it
window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});

// Display a confirmation message when the user tries to close the browser or tab
window.addEventListener('beforeunload', (event) => {
    const confirmationMessage = "Are you sure you want to leave? Your work may not be saved.";
    event.returnValue = confirmationMessage; // Standard for most browsers
    return confirmationMessage; // For some older browsers
});
