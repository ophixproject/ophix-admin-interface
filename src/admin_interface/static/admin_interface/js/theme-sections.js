(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.theme-section-heading').forEach(function (heading) {
            heading.addEventListener('click', function () {
                heading.classList.toggle('section-collapsed');
                var body = heading.nextElementSibling;
                if (body) body.classList.toggle('section-collapsed');
            });
        });
    });
}());
