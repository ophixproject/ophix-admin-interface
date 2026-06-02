(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // Collapsible section headings
        document.querySelectorAll('.theme-section-heading').forEach(function (heading) {
            heading.addEventListener('click', function (e) {
                // Don't collapse when clicking the Rename checkbox inside the heading area
                if (e.target.type === 'checkbox') return;
                heading.classList.toggle('section-collapsed');
                var body = heading.nextElementSibling;
                if (body) body.classList.toggle('section-collapsed');
            });
        });

        // Theme name protection — readonly by default for existing themes
        var nameUnlock = document.getElementById('name-unlock-checkbox');
        var nameInput  = document.getElementById('id_name');
        if (nameUnlock && nameInput) {
            var nameErrors = nameInput.closest('.col-field') &&
                             nameInput.closest('.col-field').querySelector('.errorlist');
            if (nameErrors) {
                // Form was re-displayed with errors — auto-unlock so user can correct
                nameUnlock.checked = true;
            } else {
                nameInput.setAttribute('readonly', 'readonly');
                nameInput.classList.add('theme-name-locked');
            }
            nameUnlock.addEventListener('change', function () {
                if (this.checked) {
                    nameInput.removeAttribute('readonly');
                    nameInput.classList.remove('theme-name-locked');
                    nameInput.focus();
                    nameInput.select();
                } else {
                    nameInput.setAttribute('readonly', 'readonly');
                    nameInput.classList.add('theme-name-locked');
                }
            });
        }

    });
}());
