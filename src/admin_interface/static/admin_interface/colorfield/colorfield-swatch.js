(function () {
    'use strict';

    // Run after window.load so Coloris has wrapped all [data-coloris] inputs
    // with .clr-field divs and swatch buttons, and colorfield.js has called setInstance.
    // setTimeout 0 defers us past all synchronous load handlers.
    window.addEventListener('load', function () {
        setTimeout(function () {
            document.querySelectorAll('.clr-field').forEach(function (wrapper) {
                var colorisEl = wrapper.querySelector('.colorfield_field.coloris');
                if (!colorisEl) { return; }

                // Build a plain text input for manual hex editing.
                // Inserted BEFORE the wrapper so it appears left of the swatch.
                var textEl = document.createElement('input');
                textEl.type = 'text';
                textEl.name = colorisEl.name;   // takes over form submission
                textEl.value = colorisEl.value;
                textEl.className = 'colorfield-text';
                textEl.style.width = '4em';
                textEl.placeholder = '#000000';
                if (colorisEl.required) { textEl.required = true; }
                if (colorisEl.disabled) { textEl.disabled = true; }

                wrapper.parentNode.insertBefore(textEl, wrapper);

                // Remove name from colorisEl so only textEl submits.
                // Keep colorisEl positioned and sized so Coloris can locate it
                // for picker positioning — but invisible and non-interactive.
                colorisEl.removeAttribute('name');
                wrapper.style.position = 'relative';
                colorisEl.style.cssText = (
                    'position:absolute;top:0;left:0;width:100%;height:100%;' +
                    'opacity:0;pointer-events:none;z-index:-1;'
                );

                // Coloris picked a colour → sync to textEl.
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
