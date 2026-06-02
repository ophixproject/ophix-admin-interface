(function () {
    'use strict';

    function updatePreview(container, img) {
        var bgInput  = document.querySelector('#id_css_header_background_color');
        var maxHInput = document.querySelector('#id_logo_max_height');
        var maxWInput = document.querySelector('#id_logo_max_width');

        if (bgInput && bgInput.value) {
            container.style.backgroundColor = bgInput.value;
        }

        var maxH = maxHInput ? parseInt(maxHInput.value, 10) : 0;
        var maxW = maxWInput ? parseInt(maxWInput.value, 10) : 0;

        if (maxH > 0) {
            container.style.height = (maxH + 20) + 'px';
            img.style.maxHeight = maxH + 'px';
        }
        if (maxW > 0) {
            img.style.maxWidth = maxW + 'px';
            container.style.maxWidth = (maxW + 24) + 'px';
        } else {
            container.style.maxWidth = '';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var container = document.getElementById('logo-preview-container');
        var img       = document.getElementById('logo-preview-img');
        if (!container || !img) return;

        function update() { updatePreview(container, img); }
        update();

        // Live update when the user changes header background colour or size fields.
        // ColorField syncs the native colour picker → text input so listening to the
        // text input alone covers both entry paths; also add 'change' for programmatic
        // updates from the colour picker.
        ['#id_css_header_background_color', '#id_logo_max_height', '#id_logo_max_width'].forEach(function (sel) {
            var el = document.querySelector(sel);
            if (el) {
                el.addEventListener('input', update);
                el.addEventListener('change', update);
            }
        });

        // Preview a newly selected logo file before saving.
        var fileInput = document.querySelector('#id_logo');
        if (fileInput) {
            fileInput.addEventListener('change', function () {
                if (this.files && this.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        img.src = e.target.result;
                        img.style.display = '';
                    };
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    });
}());
