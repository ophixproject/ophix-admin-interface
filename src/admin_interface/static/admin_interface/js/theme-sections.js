(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // Collapsible section headings with localStorage persistence
        document.querySelectorAll('.theme-section-heading').forEach(function (heading) {
            var body    = heading.nextElementSibling;
            var section = heading.closest('fieldset.theme-custom-section');
            var key     = section ? 'theme-section-' + section.id : null;

            // Restore saved state
            if (key && localStorage.getItem(key) === 'collapsed') {
                heading.classList.add('section-collapsed');
                if (body) body.classList.add('section-collapsed');
            }

            heading.addEventListener('click', function (e) {
                if (e.target.type === 'checkbox') return;
                var nowCollapsed = heading.classList.toggle('section-collapsed');
                if (body) body.classList.toggle('section-collapsed');
                if (key) localStorage.setItem(key, nowCollapsed ? 'collapsed' : 'expanded');
            });
        });

        // Theme name Rename toggle — readonly is set in HTML; JS only handles the checkbox
        var nameUnlock = document.getElementById('name-unlock-checkbox');
        var nameInput  = document.getElementById('id_name');
        if (nameUnlock && nameInput) {
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
