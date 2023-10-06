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

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});
