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
                if (!event.target.value) return;
                // ophix-server-base's custom.js persists changelist filter
                // state in localStorage (keyed by pathname) and silently
                // restores it whenever a changelist loads with no filter
                // params in the URL -- UNLESS this exact sessionStorage key
                // was set first. Its own click handler sets this when the
                // "Clear all filters" link (or the last remaining filter's
                // own "X" removal link) is clicked, since those are plain
                // <a href="?"> anchors it can bind to directly. A
                // dropdown-driven selection (including "All") never goes
                // through that handler at all -- it navigates via this
                // window.location assignment instead -- so without this,
                // selecting "All" here would clear the URL correctly for a
                // moment, then get silently overwritten back to the old
                // filtered URL the instant that script's own check runs on
                // the next page load. Key format intentionally mirrors
                // custom.js's own 'ophix-filter-reset:' + pathname exactly;
                // kept in sync by hand since the two live in separate
                // packages.
                try {
                    sessionStorage.setItem('ophix-filter-reset:' + window.location.pathname, '1');
                } catch (e) {}
                window.location = event.target.value;
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
