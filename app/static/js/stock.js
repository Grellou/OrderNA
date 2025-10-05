// Stock editing via admin panel
document.addEventListener("DOMContentLoaded", function () {
  function attachStockEditHandlers(context) {
    (context || document)
      .querySelectorAll(".stock-edit-form")
      .forEach(function (form) {
        // Remove any previous handler to avoid duplicates
        if (form._stockEditHandler) {
          form.removeEventListener("submit", form._stockEditHandler);
        }
        form._stockEditHandler = async function (e) {
          e.preventDefault();
          const formData = new FormData(form);
          try {
            const response = await fetch(form.action, {
              method: "POST",
              body: formData,
              headers: { "X-Requested-With": "XMLHttpRequest" },
            });
            if (response.ok) {
              const html = await response.text();
              // Replace the entire row with updated HTML
              const temp = document.createElement("tbody");
              temp.innerHTML = html.trim();
              const newRow = temp.firstElementChild;
              const row = form.closest("tr");
              if (row && newRow) {
                row.parentNode.replaceChild(newRow, row);
                // Attach handlers to new forms in the replaced row
                attachStockEditHandlers(newRow);
              }
            } else {
              const errorMsg = await response.text();
              showError(form, errorMsg || "Error updating stock");
            }
          } catch (err) {
            showError(form, "Network error");
          }
        };
        form.addEventListener("submit", form._stockEditHandler);
      });
  }

  function showError(form, message) {
    let errorSpan = form.querySelector(".error-message");
    if (!errorSpan) {
      errorSpan = document.createElement("span");
      errorSpan.className = "error-message";
      form.appendChild(errorSpan);
    }
    errorSpan.textContent = message;
  }

  attachStockEditHandlers();
});

// Seach functionality
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("stock-search");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const filter = searchInput.value.toLowerCase();
      document.querySelectorAll("#results tr").forEach(function (row) {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
      });
    });
  }

  // Sorting functionality
  document.querySelectorAll("th.sortable").forEach(function (header, colIndex) {
    header.style.cursor = "pointer";
    header.addEventListener("click", function () {
      const table = header.closest("table");
      const tbody = table.querySelector("tbody");
      const rows = Array.from(tbody.querySelectorAll("tr"));
      const isAsc = header.classList.toggle("asc");
      header.classList.toggle("desc", !isAsc);

      // Remove sort classes from other headers
      table.querySelectorAll("th.sortable").forEach(function (th) {
        if (th !== header) th.classList.remove("asc", "desc");
      });

      rows.sort(function (a, b) {
        const cellA = a.children[colIndex].textContent.trim();
        const cellB = b.children[colIndex].textContent.trim();
        // Try to compare as numbers, fallback to string
        const numA = parseFloat(cellA.replace(/[^0-9.-]+/g, ""));
        const numB = parseFloat(cellB.replace(/[^0-9.-]+/g, ""));
        if (!isNaN(numA) && !isNaN(numB)) {
          return isAsc ? numA - numB : numB - numA;
        }
        return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
      });

      // Re-attach sorted rows
      rows.forEach(function (row) {
        tbody.appendChild(row);
      });
    });
  });
});
