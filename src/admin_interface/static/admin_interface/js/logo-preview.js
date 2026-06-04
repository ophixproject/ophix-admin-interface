(function () {
    'use strict';

    function isDarkMode() {
        return document.documentElement.getAttribute('data-theme') === 'dark';
    }

    // Returns the appropriate color value for a field pair, respecting dark mode.
    function resolveColor(lightSel, darkUseSel, darkSel) {
        var lightInput   = document.querySelector(lightSel);
        var darkUseInput = document.querySelector(darkUseSel);
        var darkInput    = document.querySelector(darkSel);
        if (isDarkMode() && darkUseInput && darkUseInput.checked && darkInput && darkInput.value) {
            return darkInput.value;
        }
        return lightInput ? lightInput.value : '';
    }

    function updatePreview(container, img) {
        var maxHInput = document.querySelector('#id_logo_max_height');
        var maxWInput = document.querySelector('#id_logo_max_width');

        var bgColor = resolveColor(
            '#id_css_header_background_color',
            '#id_css_header_background_color_dark_use',
            '#id_css_header_background_color_dark'
        );
        if (bgColor) { container.style.backgroundColor = bgColor; }

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
        var checkbox = document.querySelector('#id_logo_visible[type="checkbox"]');
        img.style.display = (checkbox && !checkbox.checked) ? 'none' : '';
    }

    function syncTitleFont() {
        var titleEl       = document.getElementById('logo-preview-title');
        var headerSpan    = document.querySelector('#site-name span');
        var fontSizeInput = document.querySelector('#id_title_font_size');
        if (!titleEl) return;
        if (fontSizeInput && fontSizeInput.value.trim()) {
            titleEl.style.fontSize = fontSizeInput.value.trim();
        } else if (headerSpan) {
            titleEl.style.fontSize = window.getComputedStyle(headerSpan).fontSize;
        }
        if (headerSpan) {
            titleEl.style.fontWeight = window.getComputedStyle(headerSpan).fontWeight;
        }
    }

    function updateTitleColor() {
        var titleEl = document.getElementById('logo-preview-title');
        if (!titleEl) return;
        var color = resolveColor(
            '#id_title_color',
            '#id_title_color_dark_use',
            '#id_title_color_dark'
        );
        if (color) { titleEl.style.color = color; }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var container = document.getElementById('logo-preview-container');
        var img       = document.getElementById('logo-preview-img');
        if (!container || !img) return;

        function update() { updatePreview(container, img); }

        function updateAll() {
            update();
            updateTitleColor();
        }

        update();
        updateOffset(img);
        updateLogoVisibility(img);
        syncTitleFont();
        updateTitleColor();

        // Re-run all color updates when dark mode is toggled.
        new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                if (m.attributeName === 'data-theme') { updateAll(); }
            });
        }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

        // Live update: background colour (light + dark pair) and logo size constraints.
        ['#id_css_header_background_color', '#id_logo_max_height', '#id_logo_max_width',
         '#id_css_header_background_color_dark',
        ].forEach(function (sel) {
            var el = document.querySelector(sel);
            if (el) {
                el.addEventListener('input', update);
                el.addEventListener('change', update);
            }
        });
        var bgDarkUse = document.querySelector('#id_css_header_background_color_dark_use');
        if (bgDarkUse) { bgDarkUse.addEventListener('change', update); }

        // Live update: title font size.
        var fontSizeInput = document.querySelector('#id_title_font_size');
        if (fontSizeInput) {
            fontSizeInput.addEventListener('input',  syncTitleFont);
            fontSizeInput.addEventListener('change', syncTitleFont);
        }

        // Live update: logo visible toggle (checkbox hidden; kept for future use).
        var visibleCheckbox = document.querySelector('#id_logo_visible[type="checkbox"]');
        if (visibleCheckbox) {
            visibleCheckbox.addEventListener('change', function () { updateLogoVisibility(img); });
        }

        // Live update: vertical offset.
        var offsetInput = document.querySelector('#id_logo_vertical_offset');
        if (offsetInput) {
            offsetInput.addEventListener('input',  function () { updateOffset(img); });
            offsetInput.addEventListener('change', function () { updateOffset(img); });
        }

        // Live update: title colour (light + dark pair).
        ['#id_title_color', '#id_title_color_dark'].forEach(function (sel) {
            var el = document.querySelector(sel);
            if (el) {
                el.addEventListener('input',  updateTitleColor);
                el.addEventListener('change', updateTitleColor);
            }
        });
        var titleDarkUse = document.querySelector('#id_title_color_dark_use');
        if (titleDarkUse) { titleDarkUse.addEventListener('change', updateTitleColor); }

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
