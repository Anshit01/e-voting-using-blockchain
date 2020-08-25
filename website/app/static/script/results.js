var colorList = [
    '#f95738',
    '#22577a',
    '#9f86c0',
    '#57cc99',
    '#ee4266',
    '#ebebeb',
    '#ff67f0',
    '#41ead4',
    '#0ead69',
    '#ff9505',
    '#562c2c',
    '#a53860',
]

function fetchResult(){
    $.get('/api/get_result').done(function(res) {
        $('.load-screen').fadeOut()
        $('.whole').fadeIn()
        var partyList = []
        var voteList = []
        var tableStr = ""
        var i = 1
        res.sort(function(a, b) {return b['votes'] - a['votes']})
        for(candidate of res){
            if(candidate['votes'] != 0){
                partyList.push(candidate['party'])
                voteList.push(candidate['votes'])
            }
            tableStr += " <tr> <td class='d-none d-sm-table-cell'>" + i + "</td> <td>" + candidate['name'] + "</td> <td>" +
            candidate['party'] + "</td> <td>" + candidate['votes'] + "</td> </tr>"
            i++
        }
        document.getElementById('table-body').innerHTML += tableStr
        createGraph(partyList, voteList)
    })
}

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