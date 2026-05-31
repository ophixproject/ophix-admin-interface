(function () {
    'use strict';

    window.addEventListener('load', function () {
        setTimeout(function () {
            document.querySelectorAll('.clr-field').forEach(function (wrapper) {
                var colorisEl = wrapper.querySelector('.colorfield_field.coloris');
                if (!colorisEl) { return; }

                // Build a plain text input for manual hex editing.
                // Inserted INSIDE the wrapper after the swatch button so it sits
                // in the same layout context — the button's absolute CSS positions
                // it at the right edge of the wrapper, textEl fills the rest.
                var textEl = document.createElement('input');
                textEl.type = 'text';
                textEl.name = colorisEl.name;
                textEl.value = colorisEl.value;
                textEl.className = 'colorfield-text';
                textEl.placeholder = '#000000';
                if (colorisEl.required) { textEl.required = true; }
                if (colorisEl.disabled) { textEl.disabled = true; }

                var swatchBtn = wrapper.querySelector('button');
                wrapper.insertBefore(textEl, swatchBtn ? swatchBtn.nextSibling : colorisEl);

                // Collapse colorisEl to zero width — keeps it in the flow so
                // Coloris can read its position for picker placement, but invisible.
                colorisEl.removeAttribute('name');
                colorisEl.style.cssText = (
                    'visibility:hidden;pointer-events:none;' +
                    'width:0;min-width:0;padding:0;border:none;margin:0;'
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
