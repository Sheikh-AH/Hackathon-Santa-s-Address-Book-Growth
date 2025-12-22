function initMap() {
  console.log('Initializing map');
  
  const paths = document.querySelectorAll('#world-map path');
  console.log('Paths found:', paths.length);
  
  // Create tooltip element
  const tooltip = document.createElement('div');
  tooltip.className = 'map-tooltip';
  document.body.appendChild(tooltip);
  
  paths.forEach(path => {
    if (!path.id) return;

    // Set default fill color
    path.style.fill = '#ececec';
    path.style.cursor = 'pointer';
    path.style.transition = 'fill 0.2s ease';

    const label = path.getAttribute('name') || path.id;

    // Hover for tooltip and color change
    path.addEventListener('mouseenter', (e) => {
      path.style.fill = '#4da3ff';
      tooltip.textContent = label;
      tooltip.style.display = 'block';
    });

    path.addEventListener('mousemove', (e) => {
      tooltip.style.left = e.pageX + 10 + 'px';
      tooltip.style.top = e.pageY + 10 + 'px';
    });

    path.addEventListener('mouseleave', () => {
      path.style.fill = '#ececec';
      tooltip.style.display = 'none';
    });

    // Click
    path.addEventListener('click', () => {
      const countryName = (path.getAttribute('name') || path.id);
      const url = `/countries/${countryName}`;
      console.log('Navigating to:', url);
      window.location.href = url;
    });
  });
}

// Run immediately if DOM is already loaded, otherwise wait
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initMap);
} else {
  initMap();
}