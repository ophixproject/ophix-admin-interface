(function() {
    document.addEventListener('DOMContentLoaded', function() {
        var $ = window.django && window.django.jQuery;
        document.querySelectorAll('.list-filter-dropdown select').forEach(function(select) {
            if (select.dataset.filterInitialized) return;
            select.dataset.filterInitialized = '1';
            select.addEventListener('change', function(event) {
                if (event.target.value) window.location = event.target.value;
            });
            if ($ && typeof $.fn.select2 === 'function') {
                $(select).select2({
                    minimumResultsForSearch: Infinity,
                    width: 'resolve',
                });
            }
        });
    });
})();
