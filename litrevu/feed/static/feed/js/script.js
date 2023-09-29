document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image-input');

    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const fileName = this.files[0].name;
            const fileNameDisplay = document.querySelector('.file-name');
            fileNameDisplay.textContent = fileName;
        });
    }
});
