var colorList = [
    '#e6194b',
    '#3cb44b',
    '#ffe119',
    '#4363d8',
    '#f58231',
    '#911eb4',
    '#46f0f0',
    '#f032e6',
    '#bcf60c',
    '#fabebe',
    '#008080',
    '#e6be00',
    '#9a6324',
    '#fffac8',
    '#800000',
    '#aaffc3',
    '#808000',
    '#ffd8b1',
    '#000075',
    '#808080'
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
            title: {
                display: true,
                text: 'Vote Distribution',
                fontSize: 22,
                fontStyle: 'bold'
            },
            aspectRatio: 0.75,
            legend: {
                labels: {
                    fontSize: 16
                }
            }
        }
    })
}