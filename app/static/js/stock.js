// STOCK EDITING VIA ADMIN PANEL
document.addEventListener("DOMContentLoaded", function () {
  // Attach submit event handler to all forms in class "stock-edit-form"
  function attachStockEditHandlers(context) {
    // Search context or full document if not provided
    (context || document)
      .querySelectorAll(".stock-edit-form")
      .forEach(function (form) {
        // Remove any previous handler to avoid duplicates
        if (form._stockEditHandler) {
          form.removeEventListener("submit", form._stockEditHandler);
        }
        // Define the submit event handler for the form
        form._stockEditHandler = async function (e) {
          e.preventDefault(); // Prevent default form submission
          const formData = new FormData(form); // Gather form data
          try {
            // Send form data to server
            const response = await fetch(form.action, {
              method: "POST",
              body: formData,
              headers: { "X-Requested-With": "XMLHttpRequest" },
            });
            if (response.ok) {
              // On success response get returned HTML
              const html = await response.text();
              // Temp tbody to parse returned HTML
              const temp = document.createElement("tbody");
              temp.innerHTML = html.trim();
              const newRow = temp.firstElementChild; // New tr element
              const row = form.closest("tr"); // Find current table row containing the form
              if (row && newRow) {
                // Replace the old row with the new one from the server
                row.parentNode.replaceChild(newRow, row);
                // Attach handlers to new forms in the replaced row
                attachStockEditHandlers(newRow);
              }
            } else {
              // Show error
              const errorMsg = await response.text();
              showError(form, errorMsg || "Error updating stock");
            }
          } catch (err) {
            // Show error
            showError(form, "Network error");
          }
        };
        // Attach submit event handler to the form
        form.addEventListener("submit", form._stockEditHandler);
      });
  }

  // Displays an error message below the form
  function showError(form, message) {
    // Try to find an existing error message span
    let errorSpan = form.querySelector(".error-message");
    if (!errorSpan) {
      // If not found, create one and append to the form
      errorSpan = document.createElement("span");
      errorSpan.className = "error-message";
      form.appendChild(errorSpan);
    }
    // Set the error message text
    errorSpan.textContent = message;
  }

  // Attach handler to all forms on initial load
  attachStockEditHandlers();
});

// SEARCH FUNCTIONALITY
document.addEventListener("DOMContentLoaded", function () {
  // Get search input element by it's id
  const searchInput = document.getElementById("stock-search");
  if (searchInput) {
    // Add event listener for when user types in the search bar
    searchInput.addEventListener("input", function () {
      const filter = searchInput.value.toLowerCase(); // Search term in lowercase
      document.querySelectorAll("#results .col-md-4").forEach(function (row) {
        const text = row.textContent.toLowerCase(); // Row text in lowercase
        // Show row if it contains search term, otherwise hide it
        row.style.display = text.includes(filter) ? "" : "none";
      });
    });
  }

  // SORTING FUNCTIONALITY
  document.querySelectorAll("th.sortable").forEach(function (header, colIndex) {
    header.style.cursor = "pointer"; // Make cursor pointer clickable
    // Add click event listener to the header
    header.addEventListener("click", function () {
      const table = header.closest("table"); // Find closest table element
      const tbody = table.querySelector("tbody"); // Get table body
      const rows = Array.from(tbody.querySelectorAll("tr")); // Get all rows in the tbody
      const isAsc = header.classList.toggle("asc"); // Toggle sorting direction
      header.classList.toggle("desc", !isAsc);

      // Remove sort classes from other headers
      table.querySelectorAll("th.sortable").forEach(function (th) {
        if (th !== header) th.classList.remove("asc", "desc");
      });

      // Sort rows based on column
      rows.sort(function (a, b) {
        const cellA = a.children[colIndex].textContent.trim();
        const cellB = b.children[colIndex].textContent.trim();
        // Try to compare as numbers, fallback to string
        const numA = parseFloat(cellA.replace(/[^0-9.-]+/g, ""));
        const numB = parseFloat(cellB.replace(/[^0-9.-]+/g, ""));
        if (!isNaN(numA) && !isNaN(numB)) {
          // If both cells are numbers, compare numerically
          return isAsc ? numA - numB : numB - numA;
        }
        // Otherwise, compare as strings
        return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
      });

      // Re-attach sorted rows
      rows.forEach(function (row) {
        tbody.appendChild(row);
      });
    });
  });
});
