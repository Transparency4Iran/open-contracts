export default class Controller {
  constructor(executor, contracts, distribution, $rootScope) {
    'ngInject';
    this.executor = executor;
    this.contracts = contracts;
    var draw = function () {
      var cityData = new google.visualization.DataTable();
      cityData.addColumn('number', 'latitude'); // Implicit series 1 data col.
      cityData.addColumn('number', 'longitude'); // Implicit series 1 data col.
      cityData.addColumn('string', 'tooltip');  // Implicit series 1 data col.
      cityData.addColumn('number', 'Value'); // Implicit series 1 data col.
      cityData.addColumn({ type: 'string', role: 'tooltip' }); //
      let cityRows = _.map(_.reject(contracts.results, i => {
        return i.city === null || typeof i.city.province == "string" && i.city.province.indexOf('سایر') > -1 || i.city.lat === null;
      }), item => {
        return [Number(item.city.lat), Number(item.city.lon), item.city.name, item.price, item.price + ' ریال'];
      });
      cityData.addRows(cityRows);
      var cityChart = new google.visualization.GeoChart(document.getElementById('map'));
      cityChart.draw(cityData, {
        // width: 1024,
        // height: 640,
        region: "IR",
        resolution: "provinces",
        colorAxis: { colors: ['yellow', 'red'] },
        displayMode: 'markers'
      });

    };
    google.charts.load('current', { 'packages': ['geochart'], 'callback': draw });
    $rootScope.percentile(distribution, executor.sum);
  }
}