var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'doughnut',

    // The data for our dataset
    data: {
        labels: ['Прогнозируемый простой', 'Безвозвратный простой', 'Загрузка на день', 'Выполнено'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: [
                    "#455C73",
                    "#9B59B6",
                    "#BDC3C7",
                    "#26B99A",
            ],
            data: [50, 20, 10, 20]
        }],
    },

    // Configuration options go here
    options: {}
});