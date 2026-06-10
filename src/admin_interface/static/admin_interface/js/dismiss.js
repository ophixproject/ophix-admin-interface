(function () {
    function addDismissButtons() {
        document.querySelectorAll("ul.messagelist li").forEach(function (li) {
            if (li.querySelector(".msg-dismiss")) return;
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "msg-dismiss";
            btn.setAttribute("aria-label", "Dismiss");
            btn.textContent = "×";
            btn.addEventListener("click", function () {
                var ul = li.parentNode;
                li.remove();
                if (ul && !ul.querySelector("li")) ul.remove();
            });
            li.appendChild(btn);
        });
    }

    function scheduleAutohide() {
        var cfg = window.OPHIX_AUTOHIDE;
        if (!cfg || !cfg.enabled) return;
        document.querySelectorAll("ul.messagelist li").forEach(function (li) {
            if (!li.classList.contains("success") && !li.classList.contains("info")) return;
            var timer = setTimeout(function () {
                var ul = li.parentNode;
                li.remove();
                if (ul && !ul.querySelector("li")) ul.remove();
            }, cfg.delay);
            li.addEventListener("mouseenter", function () { clearTimeout(timer); });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            addDismissButtons();
            scheduleAutohide();
        });
    } else {
        addDismissButtons();
        scheduleAutohide();
    }
}());
