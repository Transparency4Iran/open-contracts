import BootstrapComponent from './main-directive';
import BootstrapConfig from './config';
import BootstrapRun from './run';
import '../directives/navigation/module';
import '../directives/footer/module';
import '../services/contract/module';
import '../states/index/module';
import '../states/errors/module';
import '../states/home/module';
import '../states/list/module';
import '../states/executors/module';
import '../states/executor/module';
import '../states/organization/module';
import '../states/export/module';
import '../states/contract/module';
import '../states/map/module';
import '../states/about/module';
import '../states/donate/module';
import moment from 'moment-jalaali';
import 'angular-ui-router/lib/legacy/stateEvents';
import { formatPrice } from './utils';

export default angular
  .module('omid.app', [
    'ui.router.state.events',
    'omid.directives.navigation',
    'omid.directives.footer',
    'omid.services.contracts',
    'omid.states.index',
    'omid.states.errors',
    'omid.states.home',
    'omid.states.list',
    'omid.states.executors',
    'omid.states.executor',
    'omid.states.organization',
    'omid.states.export',
    'omid.states.contract',
    'omid.states.map',
    'omid.states.about',
    'omid.states.donate',
  ])
  .config(BootstrapConfig)
  .run(BootstrapRun)
  .directive('omidBootstrap', () => new BootstrapComponent())
  .filter('dateDiff', function () {
    return function (date1, date2) {
      let j1 = moment(date1, 'YYYY-MM-DD');
      let j2 = moment(date2, 'YYYY-MM-DD');
      let yearDiff = j2.jYear() - j1.jYear();
      let monthDiff = j2.jMonth() - j1.jMonth();
      let dayDiff = j2.jDate() - j1.jDate();
      if (dayDiff < 0) {
        let tempDate = angular.copy(j2);
        tempDate.subtract(1, 'jMonth');
        const days = moment.jDaysInMonth(tempDate.jYear(), tempDate.jMonth());
        dayDiff = days + dayDiff;
        monthDiff -= 1;
      }
      if (monthDiff < 0) {
        monthDiff = monthDiff + 12;
        yearDiff = yearDiff - 1;
      }
      let ans = "";
      if (yearDiff > 0) {
        ans += yearDiff;
        ans += " سال";
        if (monthDiff > 0 || dayDiff > 0) {
          ans += " و ";
        }
      }
      if (monthDiff > 0) {
        ans += monthDiff;
        ans += " ماه";
        if (dayDiff > 0) {
          ans += ' و ';
        }
      }
      if (dayDiff > 0) {
        ans += dayDiff;
        ans += ' روز';
      }
      return ans;
    };
  }).filter('moment', function () {
    return function (date) {
      if (date) {
        return moment(date, 'YYYY-MM-DD');
      }
      return null;
    };
  }).filter('jalali', function () {
    return function (m) {
      if (m) {
        return m.format('jYYYY/jM/jD');
      }
      return null;
    };
  }).filter('jalaliWithDay', function () {
    return function (m) {
      if (m) {
        return m.format('dddd jD jMMMM jYYYY');
      }
      return null;
    };
  }).filter('price', function () {
    return formatPrice;
  }).filter('characters', function () {
    return function (input, chars, breakOnWord) {
      if (isNaN(chars)) {
        return input;
      }
      if (chars <= 0) {
        return '';
      }
      if (input && input.length > chars) {
        input = input.substring(0, chars);

        if (!breakOnWord) {
          var lastspace = input.lastIndexOf(' ');
          // get last space

          if (lastspace !== -1) {
            input = input.substr(0, lastspace);
          }
        } else {
          while (input.charAt(input.length - 1) === ' ') {
            input = input.substr(0, input.length - 1);
          }
        }
        return input + '…';
      }
      return input;
    };
  })
  .filter('pNumber', () => text => text ? persianJs(text.toString()).englishNumber().toString() : '')
  .directive('countTo', ['$timeout', function ($timeout) {
    return {
      replace: false,
      scope: true,
      link: function (scope, element, attrs) {

        var e = element[0];
        var num, refreshInterval, duration, steps, step, countTo, value, increment;

        var calculate = function () {
          refreshInterval = 30;
          step = 0;
          scope.timoutId = null;
          countTo = parseInt(attrs.countTo) || 0;
          scope.value = parseInt(attrs.value, 10) || 0;
          duration = (parseFloat(attrs.duration) * 1000) || 0;

          steps = Math.ceil(duration / refreshInterval);
          increment = ((countTo - scope.value) / steps);
          num = scope.value;
        }

        var tick = function () {
          scope.timoutId = $timeout(function () {
            num += increment;
            step++;
            if (step >= steps) {
              $timeout.cancel(scope.timoutId);
              num = countTo;
              e.textContent = persianJs(countTo.toString()).englishNumber().toString();
            } else {
              e.textContent = persianJs(Math.round(num).toString()).englishNumber().toString();
              tick();
            }
          }, refreshInterval);

        }

        var start = function () {
          if (scope.timoutId) {
            $timeout.cancel(scope.timoutId);
          }
          calculate();
          tick();
        }

        attrs.$observe('countTo', function (val) {
          if (val) {
            start();
          }
        });

        return true;
      }
    }
  }])
  .name;
