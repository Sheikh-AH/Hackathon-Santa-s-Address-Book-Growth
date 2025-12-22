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
