var colorList = [
    '#22577a',
    '#f95738',
    '#9f86c0',
    '#57cc99',
    '#ee4266',
    '#ebebeb',
    '#ff6700',
    '#41ead4',
    '#0ead69',
    '#ff9505',
    '#562c2c',
    '#a53860',
]

function createGraph(partyList, voteList) {
    var ctx = document.getElementById('pie-chart').getContext('2d')
    var pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: partyList,
            datasets: [{
                label: '# of votes',
                data: voteList,
                backgroundColor: colorList
            }]
        },
        options: {
            aspectRatio: 1,
            legend: {
                labels: {
                    fontSize: 16
                }
            }
        }
    })
}