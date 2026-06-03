(function () {
    'use strict';

    function updatePreview(container, img) {
        var bgInput   = document.querySelector('#id_css_header_background_color');
        var maxHInput = document.querySelector('#id_logo_max_height');
        var maxWInput = document.querySelector('#id_logo_max_width');

        if (bgInput && bgInput.value) {
            container.style.backgroundColor = bgInput.value;
        }

        var maxH = maxHInput ? parseInt(maxHInput.value, 10) : 0;
        var maxW = maxWInput ? parseInt(maxWInput.value, 10) : 0;

        if (maxH > 0) { img.style.maxHeight = maxH + 'px'; }
        if (maxW > 0) { img.style.maxWidth  = maxW + 'px'; }
    }

    function updateOffset(img) {
        var input  = document.querySelector('#id_logo_vertical_offset');
        var offset = input ? parseInt(input.value, 10) || 0 : 0;
        img.style.transform = offset !== 0 ? 'translateY(' + (-offset) + 'px)' : '';
    }

    function updateLogoVisibility(img) {
        var checkbox = document.querySelector('#id_logo_visible');
        if (checkbox) {
            img.style.display = checkbox.checked ? '' : 'none';
        }
    }

    function updateTitleColor() {
        var titleEl = document.getElementById('logo-preview-title');
        var input   = document.querySelector('#id_title_color');
        if (titleEl && input && input.value) {
            titleEl.style.color = input.value;
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var container = document.getElementById('logo-preview-container');
        var img       = document.getElementById('logo-preview-img');
        if (!container || !img) return;

        function update() { updatePreview(container, img); }
        update();
        updateOffset(img);
        updateLogoVisibility(img);
        updateTitleColor();

        // Live update: background colour and logo size constraints.
        ['#id_css_header_background_color', '#id_logo_max_height', '#id_logo_max_width'].forEach(function (sel) {
            var el = document.querySelector(sel);
            if (el) {
                el.addEventListener('input', update);
                el.addEventListener('change', update);
            }
        });

        // Live update: logo visible toggle.
        var visibleCheckbox = document.querySelector('#id_logo_visible');
        if (visibleCheckbox) {
            visibleCheckbox.addEventListener('change', function () { updateLogoVisibility(img); });
        }

        // Live update: vertical offset.
        var offsetInput = document.querySelector('#id_logo_vertical_offset');
        if (offsetInput) {
            offsetInput.addEventListener('input',  function () { updateOffset(img); });
            offsetInput.addEventListener('change', function () { updateOffset(img); });
        }

        // Live update: title colour.
        var titleColorInput = document.querySelector('#id_title_color');
        if (titleColorInput) {
            titleColorInput.addEventListener('input',  updateTitleColor);
            titleColorInput.addEventListener('change', updateTitleColor);
        }

        // Preview a newly selected logo file before saving.
        var fileInput = document.querySelector('#id_logo');
        if (fileInput) {
            fileInput.addEventListener('change', function () {
                if (this.files && this.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        img.src = e.target.result;
                        img.style.display = '';
                    };
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    });
}());
