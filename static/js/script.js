// Car Marketplace - JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips if using Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

// Confirm delete action
function confirmDelete(itemName = "this item") {
  return confirm(`Are you sure you want to delete ${itemName}?`);
}

// Simple form validation
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (form) {
    return form.checkValidity() === false ? false : true;
  }
  return true;
}
