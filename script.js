document.addEventListener("DOMContentLoaded", function () {
  // Select all countries inside the SVG with id "world-map"
  const countries = document.querySelectorAll('#world-map path[name]');

    // Add click event to go to country page
    country.addEventListener('click', () => {
      window.location.href = `/countries/${country.id}.html`;
    });

    // Make keyboard-accessible
    country.setAttribute('tabindex', '0');
    country.setAttribute('aria-label', country.getAttribute('name'));
    country.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        window.location.href = `/countries/${country.id}.html`;
      }
    });
  });
});
