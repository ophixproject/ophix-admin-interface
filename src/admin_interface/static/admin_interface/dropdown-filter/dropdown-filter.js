(function() {
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
