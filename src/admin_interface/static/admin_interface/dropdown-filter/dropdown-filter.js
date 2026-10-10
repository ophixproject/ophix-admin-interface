(function() {
    // This file is embedded once per filter box (dropdown_filter.html's own
    // <script> tag, inside the {% for spec in cl.filter_specs %} loop in
    // change_list.html) -- a page with N filters loads and executes this
    // same script N times. Each execution registers its own
    // DOMContentLoaded listener; when it fires, N listeners all run, each
    // doing its own querySelectorAll+forEach pass. The per-element
    // `dataset.filterInitialized` guard below is meant to stop a given
    // <select> from being bound/select2()-ed more than once, but relying
    // on N independent passes to stay perfectly in sync has turned out not
    // to be safe in practice (confirmed live: selecting "All" visibly
    // navigates to the correct cleared URL, then immediately reverts to a
    // stale filtered one -- the signature of two competing handlers, one
    // computed from current state, one from stale state). Guard at the
    // top level instead, so only the FIRST of the N embedded copies ever
    // actually runs the setup below, regardless of how many <script> tags
    // reference this file.
    if (window.__ophixDropdownFilterLoaded) return;
    window.__ophixDropdownFilterLoaded = true;

    document.addEventListener('DOMContentLoaded', function() {
        var $ = window.django && window.django.jQuery;
        document.querySelectorAll('.list-filter-dropdown select').forEach(function(select) {
            if (select.dataset.filterInitialized) return;
            select.dataset.filterInitialized = '1';

            function navigate(event) {
                if (event.target.value) window.location = event.target.value;
            }

            if ($ && typeof $.fn.select2 === 'function') {
                // Select2 fires its change notification via jQuery's
                // .trigger('change') only — there is no native .change()
                // method on a <select>, so jQuery never dispatches a real
                // DOM event for it. A plain addEventListener('change', ...)
                // never sees a Select2-driven selection (including "All"),
                // so this must be bound through jQuery's own event system,
                // which also still receives genuine native change events.
                $(select).on('change', navigate);
                $(select).select2({
                    minimumResultsForSearch: Infinity,
                    width: 'resolve',
                });
            } else {
                select.addEventListener('change', navigate);
            }
        });
    });
})();
