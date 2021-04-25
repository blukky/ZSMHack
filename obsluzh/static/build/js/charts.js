
var arr = new Array();
$('div.cart').each(function () {
  arr[$(this).attr('id')] = parseFloat($(this).text().replace(',', '.'));
});

// console.log(arr);

const labels = [
    'Июль 2020 года',
    'Август 2020 года',
    'Сентябрь 2020 года',
    'Октябрь 2020 года',
    'Ноябрь 2020 года',
    'Декабрь 2020 года',
  'Январь 2021 года',
  'Февраль 2021 года',
  'Март 2021 года',
  'Апрель 2021 года',
  'Май 2021 года',
];
const data = {
  labels: labels,
  datasets: [{
    label: 'График спроса',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: arr,
  }]
};
// </block:setup>

// <block:config:0>
const config = {
  type: 'line',
  data,
  options: {}
};
// </block:config>

