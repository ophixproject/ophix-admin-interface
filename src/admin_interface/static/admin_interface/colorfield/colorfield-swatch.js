(function () {
    'use strict';

    function initSwatchOnlyPicker() {
        // Coloris wraps each colorfield input in a .clr-field div and adds a <button>
        // swatch. That button already triggers the picker via document-level delegation.
        // We suppress clicks on the text input itself so only the swatch opens the picker.
        // Cursor positioning still works because that is browser-native, not event-driven.
        document.querySelectorAll('.colorfield_field.coloris').forEach(function (input) {
            input.addEventListener('click', function (e) {
                if (!e.isTrusted) { return; } // synthetic click from swatch — let it through
                e.stopImmediatePropagation(); // blocks Coloris's direct element listener
                e.stopPropagation();           // blocks Coloris's document-level delegation
                // default is not prevented — text cursor positioning still works
            }, true); // capture phase fires before any bubble-phase listener
        });
    }

    // Run at DOMContentLoaded so our capture listeners are in place before
    // colorfield.js's window.load handler initialises Coloris on the inputs.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSwatchOnlyPicker);
    } else {
        initSwatchOnlyPicker();
    }
})();
