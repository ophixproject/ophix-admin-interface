(function() {
    function initSelect2($) {
        // FK/M2M selects in change forms.
        // Excludes .admin-autocomplete: those are autocomplete_fields handled by Django's own
        // autocomplete.js — initialising them here too creates a second Select2 container in
        // the same flex row, making both narrow.
        // width:'style' means Select2 injects no inline width — CSS controls it via flex: 1.
        $('.related-widget-wrapper select:not(.select2-hidden-accessible):not(.admin-autocomplete)').each(function() {
            $(this).select2({
                minimumResultsForSearch: 10,
                width: 'style',
            });
        });

        // Plain choice selects opted-in via Select2Widget (class vSelect2).
        $('select.vSelect2:not(.select2-hidden-accessible)').each(function() {
            $(this).select2({
                minimumResultsForSearch: Infinity,
                width: 'resolve',
            });
        });

        // Filter sidebar dropdowns.
        // Navigation via select2:select is reliable; jQuery's trigger('change') does not
        // consistently reach native addEventListener listeners wired by dropdown-filter.js.
        $('.list-filter-dropdown select:not(.select2-hidden-accessible)').each(function() {
            $(this).select2({
                minimumResultsForSearch: Infinity,
                width: 'style',
            }).on('select2:select', function(e) {
                var url = e.params.data.id;
                if (url) window.location = url;
            });
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
