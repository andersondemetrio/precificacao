// document.addEventListener("DOMContentLoaded", function () {
//     var ctx = document.getElementById('myPieChart').getContext('2d');

//     var totalTributos = parseFloat(document.getElementById('myPieChart').getAttribute('data-tot-tributos'));
//     var totalLucros = parseFloat(document.getElementById('myPieChart').getAttribute('data-tot-lucros'));

//     if (!isNaN(totalTributos) && !isNaN(totalLucros)) {
//         var data = {
//             labels: ['Impostos', 'Lucro'],
//             datasets: [{
//                 data: [totalTributos, totalLucros],
//                 backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(75, 192, 192, 0.6)']
//             }]
//         };

//         var myPieChart = new Chart(ctx, {
//             type: 'pie',
//             data: data,
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 title: {
//                     display: true,
//                     text: 'Impostos vs. Lucro'
//                 }
//             }
//         });
//     }
// });
