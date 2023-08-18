const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'bar',
    data: {
    labels: {{labels|safe}},
    datasets: [{
        label: 'Gastos por categoria',
        data: {{values}},
    }]
    },    
});
