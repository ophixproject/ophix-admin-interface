(function () {
    'use strict';

    // Run after window.load so Coloris has already wrapped all [data-coloris] inputs
    // with .clr-field divs and swatch buttons, and colorfield.js has called setInstance.
    // setTimeout 0 defers us past all synchronous load handlers.
    window.addEventListener('load', function () {
        setTimeout(function () {
            document.querySelectorAll('.clr-field').forEach(function (wrapper) {
                var colorisEl = wrapper.querySelector('.colorfield_field.coloris');
                if (!colorisEl) { return; }

                // Build a plain text input for manual hex editing.
                var textEl = document.createElement('input');
                textEl.type = 'text';
                textEl.name = colorisEl.name;   // carries the field value on submit
                textEl.value = colorisEl.value;
                textEl.className = 'colorfield-text vTextField';
                textEl.placeholder = '#000000';
                if (colorisEl.required) { textEl.required = true; }
                if (colorisEl.disabled) { textEl.disabled = true; }

                // Hand off the name so only textEl submits (colorisEl is hidden).
                colorisEl.removeAttribute('name');
                colorisEl.style.display = 'none';

                // Insert the text input immediately after the .clr-field wrapper.
                wrapper.parentNode.insertBefore(textEl, wrapper.nextSibling);

                // Coloris picked a colour → sync to the text input.
                colorisEl.addEventListener('input', function () {
                    textEl.value = colorisEl.value;
                });

                // User typed a hex value → sync to colorisEl so Coloris updates the swatch.
                textEl.addEventListener('input', function () {
                    colorisEl.value = textEl.value;
                    colorisEl.dispatchEvent(new Event('input', { bubbles: true }));
                });
            });
        }, 0);
    });
})();
