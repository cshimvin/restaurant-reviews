// Function to show tooltips
// Taken from Bootstrap documents - https://getbootstrap.com/docs/4.0/components/tooltips/
tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));