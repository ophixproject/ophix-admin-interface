(function () {
    'use strict';

    // Coloris wraps each colorfield input in .clr-field with an absolutely-positioned
    // swatch button (30px, right edge, pointer-events:none). Clicks on the button area
    // fall through to the underlying input, which Coloris listens to for openPicker().
    // We intercept clicks in the TEXT area (left of the swatch) only, so cursor
    // positioning works normally there. Swatch-area clicks pass through to Coloris.

    var SWATCH_WIDTH = 30; // matches .clr-field button { width: 30px } in coloris.css

    function initSwatchOnlyPicker() {
        document.querySelectorAll('.colorfield_field.coloris').forEach(function (input) {
            input.addEventListener('click', function (e) {
                if (e.offsetX < input.offsetWidth - SWATCH_WIDTH) {
                    // Text area — suppress Coloris's openPicker listener
                    e.stopImmediatePropagation();
                    e.stopPropagation();
                }
                // Swatch zone — let Coloris open the picker
            }, true); // capture phase fires before Coloris's bubble-phase listener
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSwatchOnlyPicker);
    } else {
        initSwatchOnlyPicker();
    }
})();
