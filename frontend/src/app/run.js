import moment from 'moment-jalaali';
import JSURL from 'jsurl';
import {formatPrice} from './utils';

export default function BootstrapRun($location, $log, $rootScope) {
  'ngInject';
  moment.loadPersian();
  $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState) {
    $rootScope.loading = true;
  });

  $rootScope.$on('$viewContentLoaded', function (event) {
    $rootScope.loading = false;
  });
  $rootScope.encodeQuery = function (query) {
    return JSURL.stringify(query);
  };
  $rootScope.percentile = function (data, target = -1) {
    var sum = _.reduce(data, function(memo, item){ return memo + item.count; }, 0);
    d3plus.viz()
      .container('.percentile_chart')
      .data(_.map(data, item => {
          item.color = 'blue';
          if (target >= item.start) {
            if (target < item.end) {
              item.color = 'green';
            }
            if (target === item.end && item.percentile === 100) {
              item.color = 'green';
            }
          }
          item['درصد']=item.count*100/sum;
          item.interval = 'از ';
          item.interval += formatPrice(item.start/1000000);
          item.interval += ' تا ';
          item.interval += formatPrice(item.end/1000000);
          item.interval += 'میلیون ریال';
          item.percentileShow = 'صدک ' + item.percentile + 'ام';
          item.temp='';
          item['تعداد قرارداد']=item.count;
          item['بازه']=item.interval;
          return item;
        }
      ))
      .type('bar')
      .id('percentileShow')
      .y({'value': 'تعداد قرارداد'})
      .x({'scale': 'discrete', 'value': 'temp', 'label': 'مبلغ'})
      .tooltip(['درصد','بازه'])
      .color('color')
      .order('percentile')
      .height(600)
      // .width(1900)
      .draw();
  }
}