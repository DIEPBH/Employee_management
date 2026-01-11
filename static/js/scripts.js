/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
// ===== TOGGLE SIDEBAR =====
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("menu-toggle");
    const wrapper = document.getElementById("wrapper");

    if (toggleBtn && wrapper) {
        toggleBtn.addEventListener("click", function () {
            wrapper.classList.toggle("toggled");
        });
    }
});

// ===== RESIZABLE TABLE COLUMNS =====
document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector(".resizable-table");
    if (!table) return;

    const cols = table.querySelectorAll("th");

    cols.forEach((th) => {
        const resizer = th.querySelector(".col-resizer");
        if (!resizer) return;

        let startX, startWidth;

        resizer.addEventListener("mousedown", function (e) {
            startX = e.pageX;
            startWidth = th.offsetWidth;

            document.addEventListener("mousemove", resizeColumn);
            document.addEventListener("mouseup", stopResize);
        });

        function resizeColumn(e) {
            const newWidth = startWidth + (e.pageX - startX);
            th.style.width = newWidth + "px";
        }

        function stopResize() {
            document.removeEventListener("mousemove", resizeColumn);
            document.removeEventListener("mouseup", stopResize);
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const fullnameCells = document.querySelectorAll(".col-fullname");

    let maxWidth = 0;

    fullnameCells.forEach(cell => {
        const span = document.createElement("span");
        span.style.visibility = "hidden";
        span.style.whiteSpace = "nowrap";
        span.style.font = window.getComputedStyle(cell).font;
        span.innerText = cell.innerText;

        document.body.appendChild(span);
        const width = span.offsetWidth;
        document.body.removeChild(span);

        if (width > maxWidth) {
            maxWidth = width;
        }
    });

    // Giới hạn để không phá layout
    const finalWidth = Math.min(maxWidth + 20, 450); // max 450px

    document.querySelectorAll(".table-canbo th:nth-child(2), .table-canbo td:nth-child(2)")
        .forEach(el => {
            el.style.width = finalWidth + "px";
            el.style.minWidth = finalWidth + "px";
        });
});

// ===== TOOLTIP =====
document.addEventListener("DOMContentLoaded", function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});