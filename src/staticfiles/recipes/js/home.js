document.addEventListener('DOMContentLoaded', function() { // Ensure the DOM is fully loaded
    clear_filters_btn = document.getElementById('clear-filters-btn');
    
    if (clear_filters_btn) {
        clear_filters_btn.addEventListener('click', function(event) {
            console.log('Clear Filters button clicked');
            event.preventDefault();
            // Redirect to home page with #recipes anchor
            window.location.href = window.location.pathname + '#recipes';
        });
    }
});   