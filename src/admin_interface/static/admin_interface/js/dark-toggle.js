(function () {
    'use strict';

    function getDarkFieldBox(checkbox) {
        var darkName = checkbox.name.replace(/_dark_use$/, '_dark');
        var darkInput = document.querySelector('[name="' + darkName + '"]');
        return darkInput ? darkInput.closest('.fieldBox') : null;
    }

    function applyToggle(checkbox) {
        var darkBox = getDarkFieldBox(checkbox);
        if (darkBox) {
            darkBox.style.display = checkbox.checked ? '' : 'none';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('input[name$="_dark_use"]').forEach(function (checkbox) {
            applyToggle(checkbox);
            checkbox.addEventListener('change', function () {
                applyToggle(checkbox);
            });
        });
    });
}());
