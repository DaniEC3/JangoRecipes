document.addEventListener('DOMContentLoaded', function() { // Ensure the DOM is fully loaded
    clear_filters_btn = document.getElementById('clear-filters-btn');
    recipes_section = document.getElementById('recipes');   
    if (clear_filters_btn) {
        clear_filters_btn.addEventListener('click', function(event) {
            console.log('Clear Filters button clicked');
            event.preventDefault();
            window.location.href = window.location.pathname;
            window.scrollTo(0, recipes_section.offsetTop);
        });
    }
});   