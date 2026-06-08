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
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", addDismissButtons);
    } else {
        addDismissButtons();
    }
}());
