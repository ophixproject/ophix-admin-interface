(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // #object-history-back-tools always renders inside #content (safe on
        // every Django version, since Django's own object_history.html never
        // gives object_tools an overridable slot within its own content block on
        // any version). On Django 6.1+, object-tools belongs alongside .titles as
        // a flex sibling in .titles-and-tools instead — relocate it there when
        // that wrapper exists. Pre-6.1 (no .titles-and-tools at all) it's left
        // exactly where it rendered, where the existing float/margin-top hack in
        // object-tools.css already positions it, matching every other
        // object-tools button on that Django version.
        var backTools = document.getElementById('object-history-back-tools');
        if (!backTools) return;
        var titlesAndTools = document.querySelector('.titles-and-tools');
        if (titlesAndTools) {
            titlesAndTools.appendChild(backTools);
        }
    });
}());
