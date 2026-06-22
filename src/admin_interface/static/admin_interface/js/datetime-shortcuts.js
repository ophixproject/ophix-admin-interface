/* Remove the "|" separator that DateTimeShortcuts.js inserts as a text node (#6c).
 * CSS cannot target text nodes, so a MutationObserver fires as shortcuts are
 * added to the DOM and strips any text node containing "|" immediately. */
(function () {
    'use strict';

    function removePipeSeparators(container) {
        container.querySelectorAll('.datetimeshortcuts').forEach(function (span) {
            Array.from(span.childNodes)
                .filter(function (n) {
                    return n.nodeType === Node.TEXT_NODE && n.textContent.indexOf('|') !== -1;
                })
                .forEach(function (n) { n.remove(); });
        });
    }

    var obs = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            mutation.addedNodes.forEach(function (node) {
                if (node.nodeType !== Node.ELEMENT_NODE) return;
                if (node.classList && node.classList.contains('datetimeshortcuts')) {
                    removePipeSeparators(node.parentElement || document);
                } else {
                    removePipeSeparators(node);
                }
            });
        });
    });

    document.addEventListener('DOMContentLoaded', function () {
        obs.observe(document.body, { childList: true, subtree: true });
    });
})();
