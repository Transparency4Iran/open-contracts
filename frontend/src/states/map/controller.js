import moment from 'moment-jalaali';
import { formatPrice } from '../../app/utils';

export default class Controller {
  constructor(topOrganizations, ContractsService) {
    'ngInject';
    this.topOrganizations = topOrganizations;
    this.service = ContractsService;
    this.ordering = '-sum';
    let $ctrl = this;
    $ctrl.chart = d3plus.viz()
      .container("#bar_chart")
      .type("bar")
      .id("province")
      .x({ 'scale': 'discrete', 'value': 'province', 'label': 'استان' })
      .y({ 'value': "sum", 'label': 'مجموع مبلغ قراردادها' })
      .order('sum')
      .height(400);
    var provinceToEnglish = function (persian) {
      switch (persian) {
        case 'تهران':
          return 'tehran';
        case 'یزد':
          return 'yazd';
        case 'البرز':
          return 'IR-32';
        case 'هرمزگان':
          return 'IR-23';
        case 'خراسان رضوی':
          return 'IR-30';
        case 'بوشهر':
          return 'IR-06';
        case 'خوزستان':
          return 'IR-10';
        case 'گیلان':
          return 'gilan';
        case 'قزوین':
          return 'IR-28';
        case 'مرکزی':
          return 'IR-22';
        case 'قم':
          return 'qom';
        case 'فارس':
          return 'fars';
        case 'اصفهان':
          return 'IR-04';
        case 'آذربایجان شرقی':
          return 'IR-01';
        case 'ایلام':
          return 'ilam';
        case 'همدان':
          return 'IR-24';
        case 'کرمانشاه':
          return 'IR-17';
        case 'خراسان جنوبی':
          return 'IR-29';
        case 'خراسان شمالی':
          return 'IR-31';
        case 'سیستان وبلوچستان':
          return 'IR-13';
        case 'مازندران':
          return 'mazandaran';
        case 'گلستان':
          return 'IR-27';
        case 'اردبیل':
          return 'IR-03';
        case 'کردستان':
          return 'IR-16';
        case 'آذربایجان غربی':
          return 'IR-02';
        case 'لرستان':
          return 'IR-20';
        case 'کرمان':
          return 'IR-15';
        case 'چهارمحال وبختیاری':
          return 'IR-08';
        case 'کهگیلویه وبویراحمد':
          return 'IR-18';
        case 'زنجان':
          return 'IR-11';
        case 'سمنان':
          return 'IR-12';
        default:
          return 'nowhere';
      }
    };
    this.query = {
      limit: 10000
    };
    this.change = function () {
      if ($ctrl.start_contract_date) {
        $ctrl.query.contract_date__gte = moment($ctrl.start_contract_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      if ($ctrl.end_contract_date) {
        $ctrl.query.contract_date__lte = moment($ctrl.end_contract_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      $ctrl.promise = $ctrl.service.getOnLocation('province', $ctrl.query).then(resp => {
        let nullProvince = _.find(resp, i => {
          return i.province === null;
        });
        let otherProvince = _.find(resp, i => {
          return i.province !== null && i.province.includes('سایر');
        });
        let sumBad = (nullProvince ? nullProvince.sum : 0) + (otherProvince ? otherProvince.sum : 0);
        let countBad = (nullProvince ? nullProvince.count : 0) + (otherProvince ? otherProvince.count : 0);
        let corrected = _.reject(resp, i => {
          return i.province === null || i.province.includes('سایر');
        });
        if (sumBad > 0) {
          corrected.push({
            province: '**سایر موارد**',
            sum: sumBad,
            count: countBad
          });
        }
        $ctrl.onProvince = corrected;
        google.charts.load('current', { 'packages': ['geochart'], 'callback': drawProvince });
        drawChart();
      });
      $ctrl.service.getOnLocation('town', $ctrl.query).then(resp => {
        $ctrl.onTown = resp;
        google.charts.load('current', { 'packages': ['geochart'], 'callback': drawTown });
      });
    };
    this.change();
    var drawProvince = function () {
      var provinceData = new google.visualization.DataTable();
      provinceData.addColumn('string', 'Country'); // Implicit domain label col.
      provinceData.addColumn('number', 'Value'); // Implicit series 1 data col.
      provinceData.addColumn({ type: 'string', role: 'tooltip' }); //
      let provinceRows = _.map(_.reject($ctrl.onProvince, i => {
        return i.province === null || i.province.includes('سایر');
      }), item => {
        let p = {
          f: item.province,
          v: provinceToEnglish(item.province)
        };
        let t = 'تعداد کل قراردادها:';
        t += item.count;
        t += '\n';
        t += 'مبلغ کل قراردادها:';
        t += formatPrice(item.sum);
        return [p, item.sum, t];
      });
      provinceData.addRows(provinceRows);
      var provinceChart = new google.visualization.GeoChart(document.getElementById('province_div'));
      provinceChart.draw(provinceData, {
        // width: 1024,
        // height: 640,
        region: "IR",
        resolution: "provinces",
        colorAxis: { colors: ['yellow', 'red'] }
      });
    }
    var drawTown = function () {
      var townData = new google.visualization.DataTable();
      townData.addColumn('number', 'latitude'); // Implicit series 1 data col.
      townData.addColumn('number', 'longitude'); // Implicit series 1 data col.
      townData.addColumn('string', 'tooltip');  // Implicit series 1 data col.
      townData.addColumn('number', 'Value'); // Implicit series 1 data col.
      townData.addColumn({ type: 'string', role: 'tooltip' }); //
      let townRows = _.map(_.reject($ctrl.onTown, i => {
        return i.town === null || i.town.province.includes('سایر') || i.town.lat === null;
      }), item => {
        let a = 'استان ';
        a += item.town.province;
        a += ' شهرستان ';
        a += item.town.name;
        let t = 'تعداد کل قراردادها:';
        t += item.count;
        t += '\n';
        t += 'مبلغ کل قراردادها:';
        t += formatPrice(item.sum);
        return [Number(item.town.lat), Number(item.town.lon), a, item.sum, t];
      });
      townData.addRows(townRows);
      var townChart = new google.visualization.GeoChart(document.getElementById('town_div'));
      townChart.draw(townData, {
        // width: 1024,
        // height: 640,
        region: "IR",
        resolution: "provinces",
        colorAxis: { colors: ['yellow', 'red'] },
        displayMode: 'markers'
      });

    };

    var drawChart = function () {
      $ctrl.chart
        .data($ctrl.onProvince)
        .draw();
    };
  }

  changeTopOrganization() {
    const top_id = this.query.top_organization;
    if (top_id) {
      this.leaves = _.findWhere(this.topOrganizations, { 'id': top_id }).leaves;
    } else {
      this.leaves = false;
    }
    this.query.organization = '';

  }

}