(function() {
    document.addEventListener('DOMContentLoaded', function() {
        var $ = window.django && window.django.jQuery;
        if (!$ || typeof $.fn.select2 !== 'function') return;
        $('.related-widget-wrapper select:not(.select2-hidden-accessible)').each(function() {
            $(this).select2({
                minimumResultsForSearch: 10,
                width: '100%',
            });
        });
    });
})();
