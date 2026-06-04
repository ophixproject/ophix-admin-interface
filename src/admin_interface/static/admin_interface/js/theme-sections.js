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

        // Custom file widgets — Choose File buttons trigger hidden inputs
        document.querySelectorAll('.theme-file-btn[data-target]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var input = document.getElementById(btn.getAttribute('data-target'));
                if (input) input.click();
            });
        });

        // File widget — update filename display when a new file is selected
        ['logo', 'favicon'].forEach(function (widgetId) {
            var fileInput = document.getElementById('id_' + widgetId);
            if (!fileInput) return;
            fileInput.addEventListener('change', function () {
                var file     = this.files[0];
                if (!file) return;
                var nameSpan = document.getElementById(widgetId + '-name');
                var clearBox = document.getElementById(widgetId + '-clear_id');
                var clearBtn = document.querySelector('.file-clear-btn[data-widget="' + widgetId + '"]');
                if (nameSpan) {
                    nameSpan.textContent = file.name;
                    nameSpan.classList.remove('file-name-empty');
                }
                if (clearBtn) clearBtn.style.display = '';
                if (clearBox) clearBox.checked = false;
            });
        });

        // File widget — X button resets to empty state (shows placeholder, hides X)
        document.querySelectorAll('.file-clear-btn[data-widget]').forEach(function (btn) {
            var widgetId = btn.getAttribute('data-widget');
            btn.addEventListener('click', function () {
                var clearBox  = document.getElementById(widgetId + '-clear_id');
                var nameSpan  = document.getElementById(widgetId + '-name');
                var fileInput = document.getElementById('id_' + widgetId);
                if (clearBox)  clearBox.checked = true;
                if (fileInput) fileInput.value = '';
                if (nameSpan) {
                    nameSpan.textContent = nameSpan.getAttribute('data-none-text') || '';
                    nameSpan.classList.add('file-name-empty');
                }
                btn.style.display = 'none';
                if (widgetId === 'logo') {
                    var img = document.getElementById('logo-preview-img');
                    if (img) img.style.display = 'none';
                }
                if (widgetId === 'favicon') {
                    var preview = document.getElementById('favicon-preview-container');
                    if (preview) preview.innerHTML = '';
                }
            });
        });

        // Strip storage path prefix — show filename only in all file-name-display spans
        document.querySelectorAll('.file-name-display').forEach(function (el) {
            var text = el.textContent.trim();
            if (text) el.textContent = text.split('/').pop();
        });

        // Theme name Rename toggle — pencil button toggles readonly on the name input
        var nameUnlockBtn = document.getElementById('name-unlock-btn');
        var nameInput     = document.getElementById('id_name');
        if (nameUnlockBtn && nameInput) {
            nameUnlockBtn.addEventListener('click', function () {
                if (nameInput.hasAttribute('readonly')) {
                    nameInput.removeAttribute('readonly');
                    nameInput.classList.remove('theme-name-locked');
                    nameUnlockBtn.classList.add('name-unlock-active');
                    nameInput.focus();
                    nameInput.select();
                } else {
                    nameInput.setAttribute('readonly', 'readonly');
                    nameInput.classList.add('theme-name-locked');
                    nameUnlockBtn.classList.remove('name-unlock-active');
                }
            });
        }

    });
}());
