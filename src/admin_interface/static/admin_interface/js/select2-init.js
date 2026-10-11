(function() {
    function initSelect2($) {
        // FK/M2M selects in change forms.
        // Excludes .admin-autocomplete: those are autocomplete_fields handled by Django's own
        // autocomplete.js — initialising them here too creates a second Select2 container in
        // the same flex row, making both narrow.
        // Excludes .selectfilter/.selectfilterstacked: Django's own class names for the
        // filter_horizontal/filter_vertical raw <select>, which its own SelectFilter2.js
        // independently converts into the dual-listbox "selector" widget -- enhancing the
        // same element with Select2 too produced a second, empty, non-functional dropdown
        // sitting beside the real widget (confirmed live 2026-10-11, Users/Groups).
        // width:'style' means Select2 injects no inline width — CSS controls it via flex: 1.
        $('.related-widget-wrapper select:not(.select2-hidden-accessible):not(.admin-autocomplete):not(.selectfilter):not(.selectfilterstacked)').each(function() {
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
        // This is the real navigator for these on every changelist page: select2
        // loads lazily (see below), which means it is never registered as a jQuery
        // plugin yet by the time dropdown-filter.js's own DOMContentLoaded handler
        // runs, so that file's select2-aware branch never actually executes here in
        // practice -- confirmed live (2026-10-11): a real mouse-driven selection
        // produces only this handler's `select2:select` event, never a jQuery
        // `change` reaching dropdown-filter.js's `navigate()`. Navigation via
        // select2:select is reliable; select2's own `change` notification is
        // jQuery-trigger-only and does not reach a native addEventListener.
        $('.list-filter-dropdown select:not(.select2-hidden-accessible)').each(function() {
            $(this).select2({
                minimumResultsForSearch: Infinity,
                width: 'style',
            }).on('select2:select', function(e) {
                var url = e.params.data.id;
                if (!url) return;
                // ophix-server-base's custom.js persists changelist filter state
                // in localStorage and silently restores it on any changelist load
                // with no filter params in the URL, unless this exact
                // sessionStorage key was set first. Setting it unconditionally
                // here is safe: custom.js only ever reads it when the resulting
                // URL has zero filter params, so it's simply ignored on every
                // navigation that leaves other filters active. Same key
                // convention as dropdown-filter.js's own (inert-on-changelists,
                // see above) copy of this -- kept in sync by hand since the two
                // live in separate packages.
                try {
                    sessionStorage.setItem('ophix-filter-reset:' + window.location.pathname, '1');
                } catch (e) {}
                window.location = url;
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
