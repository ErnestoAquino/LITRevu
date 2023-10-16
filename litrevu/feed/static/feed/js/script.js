// Update and display the name of the file selected in an image-type input.
document.addEventListener('DOMContentLoaded', function() {
    // Fetches the element with the ID 'image-input' from the DOM
    const imageInput = document.getElementById('image-input');

    // Checks if the image input element exists on the page
    if (imageInput) {
        // Attaches an event listener to the image input that fires when the value changes (i.e., a new file is chosen)
        imageInput.addEventListener('change', function() {
            // Retrieves the name of the selected file
            const fileName = this.files[0].name;
            // Fetches the element meant for displaying the file name from the DOM
            const fileNameDisplay = document.querySelector('.file-name');
            // Updates the text content of the file name display element with the chosen file's name
            fileNameDisplay.textContent = fileName;
        });
    }
});

// Allow users to close (remove) notifications by clicking on a delete button.
document.addEventListener('DOMContentLoaded', () => {
    // Fetches all the delete buttons inside notifications and converts them into an array (or an empty array if none are found)
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        // Gets the parent notification of the current delete button
        const $notification = $delete.parentNode;

        // Attaches an event listener to the delete button that fires when it's clicked
        $delete.addEventListener('click', () => {
            // Removes the parent notification from the DOM
            $notification.parentNode.removeChild($notification);
        });
    });
});
