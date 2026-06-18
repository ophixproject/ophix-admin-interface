(function() {
    function initSelect2($) {
        // FK/M2M selects in change forms
        // Use width:'style' so Select2 does not inject an inline style.width —
        // the container width is then controlled entirely by CSS.
        $('.related-widget-wrapper select:not(.select2-hidden-accessible)').each(function() {
            $(this).select2({
                minimumResultsForSearch: 10,
                width: 'style',
            });
        });
        // Filter sidebar dropdowns (no search, navigate on change)
        document.querySelectorAll('.list-filter-dropdown select').forEach(function(select) {
            if (!$(select).hasClass('select2-hidden-accessible')) {
                $(select).select2({
                    minimumResultsForSearch: Infinity,
                    width: '100%',
                });
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        var $ = window.django && window.django.jQuery;
        if (!$) return;

        if (typeof $.fn.select2 === 'function') {
            initSelect2($);
            return;
        }

        // Select2 not loaded — common on changelist pages without autocomplete_fields.
        // Temporarily restore the global jQuery so Select2's UMD wrapper can attach to it,
        // then clean up once it has.
        var loaderEl = document.getElementById('ophix-select2-loader');
        if (!loaderEl) return;
        var jsUrl = loaderEl.getAttribute('data-js');
        if (!jsUrl) return;

        window.jQuery = $;
        var script = document.createElement('script');
        script.src = jsUrl;
        script.onload = function() {
            delete window.jQuery;
            initSelect2($);
        };
        document.head.appendChild(script);
    });
})();
