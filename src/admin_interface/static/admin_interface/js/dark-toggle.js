(function () {
    'use strict';

    function getDarkFieldBox(checkbox) {
        var darkName = checkbox.name.replace(/_dark_use$/, '_dark');
        var darkInput = document.querySelector('[name="' + darkName + '"]');
        if (!darkInput) return null;
        // Custom template sections use .col-dark; standard fieldset sections use .fieldBox
        return darkInput.closest('.col-dark') || darkInput.closest('.fieldBox');
    }

    function applyToggle(checkbox) {
        var darkBox = getDarkFieldBox(checkbox);
        if (darkBox) {
            darkBox.style.display = checkbox.checked ? '' : 'none';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('input[name$="_dark_use"]').forEach(function (checkbox) {
            var formRow = checkbox.closest('.form-row');
            if (formRow) formRow.classList.add('dark-pair-row');
            applyToggle(checkbox);
            checkbox.addEventListener('change', function () {
                applyToggle(checkbox);
            });
        });
    });
}());
