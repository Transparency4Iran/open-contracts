import moment from 'moment-jalaali';
import persianjs from 'persianjs';

export default class Controller {
  constructor($scope, $timeout, ContractsService) {
    'ngInject';

    $scope.stat = {};
    $timeout(function () {
      ContractsService.getPromiseByEndpoint('aggregate/stat').then(resp => {
        $scope.stat = resp.data;
      });
      ContractsService.getPromiseByEndpoint('attempts?limit=60').then(resp => {
        let attempts = resp.data.results;
        let data = _.union(_.map(attempts, item => {
          let newItem = {};
          newItem['تاریخ'] = persianjs(moment(item.yesterday, 'YYYY-MM-DD').format('jYYYY/jMM/jDD')).englishNumber().toString();
          newItem.text = 'روند ثبت قرارداد در ماه اخیر';
          newItem['تعداد قرارداد'] = item.new_count;
          return newItem;
        }), _.map(attempts, item => {
          let newItem = {};
          newItem['تاریخ'] = persianjs(moment(item.yesterday, 'YYYY-MM-DD').format('jYYYY/jMM/jDD')).englishNumber().toString();
          newItem.text = 'روند بروز خطا در ماه اخیر';
          newItem['تعداد قرارداد'] = item.with_errors_count;
          return newItem;
        }));
        d3plus.viz()
          .container("#attempts") // container DIV to hold the visualization
          .data(data) // data to use with the visualization
          .type("line") // visualization type
          .id("text") // key for which our data is unique on
          // .text("name")       // key to use for display text
          .y('تعداد قرارداد') // key to use for y-axis
          .x("تاریخ") // key to use for x-axis
          .resize(true)
          .height(400)
          .draw();

      });
      ContractsService.getDailyFetchPerTopOrganization(60).then(resp => {
        let dailyFetchPerTopOrganization = resp.data.results;
        d3plus.viz()
          .container('#dailyFetchPerTopOrganization')
          .data(_.map(dailyFetchPerTopOrganization, function (item) {
            item.top_organization = item.top_organization.display_name;
            item['تعداد قرارداد'] = item.count
            item['تاریخ'] = persianjs(moment(item.date, 'YYYY-MM-DD').format('jYYYY/jMM/jDD')).englishNumber().toString();
            return item;
          }))
          .type('bar')
          .id('top_organization')
          .y({
            'stacked': true,
            'value': 'تعداد قرارداد'
          })
          .x({
            'scale': 'discrete',
            'value': 'تاریخ'
          })
          //
          .resize(true)
          .height(400)
          .draw();
      })
    }, 1);
  }
}
