const labels = JSON.parse('{{ labels | tojson | safe }}');
const chartData = JSON.parse('{{ data | tojson | safe }}');
const img = new Image();

const data = {
    labels: labels,
    datasets: [{
        label: 'Population ({{title}})',
        backgroundColor: 'rgb(234, 70, 48)',
        borderColor: 'rgb(187, 37, 40)',
        pointRadius: 0,
        data: chartData,
    }],
};

const config = {
    type: 'line',
    data: data,
    options: {
        scales: {
            y: {
                title: {
                    display: true,
                    text: 'Population',
                    align: 'center',
                    padding: 10
                },
                beginAtZero:true,

            },
            

            x: {
                title: {
                    display: true,
                    text: 'Year',
                    align: 'center',
                    padding: 10
                },
                ticks: {
                    maxTicksLimit: 25                       },
                
            }
        }

    }
};

const myChart = new Chart(
    document.getElementById('myChart'),
    config
);

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

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initMap);
} else {
  initMap();
}
