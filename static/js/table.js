// table.js
App.onReady(() => {
  // TOOLTIP
  if (window.bootstrap) {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
      new bootstrap.Tooltip(el);
    });
  }

  // RESIZABLE TABLE COLUMNS
  const table = document.querySelector(".resizable-table");
  if (table) {
    table.querySelectorAll("th").forEach(th => {
      const resizer = th.querySelector(".col-resizer");
      if (!resizer) return;

      let startX = 0, startWidth = 0;

      const onMove = (e) => {
        const newWidth = startWidth + (e.pageX - startX);
        th.style.width = newWidth + "px";
      };

      const onUp = () => {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
        // đồng bộ lại row height nếu đang dùng 2 bảng
        setTimeout(syncActionTableRows, 0);
      };

      resizer.addEventListener("mousedown", (e) => {
        startX = e.pageX;
        startWidth = th.offsetWidth;
        document.addEventListener("mousemove", onMove);
        document.addEventListener("mouseup", onUp);
      });
    });
  }

  // SYNC 2 TABLE ROW HEIGHTS (table-data + table-action)
  function syncActionTableRows() {
    const dataTable = document.querySelector(".table-data");
    const actionTable = document.querySelector(".table-action table.table-action");
    if (!dataTable || !actionTable) return;

    const dataHead = dataTable.querySelector("thead tr");
    const actionHead = actionTable.querySelector("thead tr");
    if (dataHead && actionHead) actionHead.style.height = dataHead.offsetHeight + "px";

    const dataRows = dataTable.querySelectorAll("tbody tr");
    const actionRows = actionTable.querySelectorAll("tbody tr");
    const n = Math.min(dataRows.length, actionRows.length);

    for (let i = 0; i < n; i++) {
      actionRows[i].style.height = dataRows[i].offsetHeight + "px";
    }
  }

  window.addEventListener("load", syncActionTableRows);
  window.addEventListener("resize", syncActionTableRows);
  document.addEventListener("mouseup", () => setTimeout(syncActionTableRows, 0));
});
