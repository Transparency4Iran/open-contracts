import jQuery from 'jquery'
import 'd3plus'

export default class Controller {
  constructor(onOrganizationYear, onOrganizationMonth, $scope) {
    'ngInject';

    $scope.renderOrganizationMonthCount = function () {
      angular.element('#chart').empty();
      $scope.chart = d3plus.viz()
        .container('#chart')
        .data(_.map(_.filter(onOrganizationMonth, i => {
          return i.year >= 1394;
        }), item => {
          item.year_month = Number(item.year + '.' + (item.month < 10 ? '0' : '') + item.month);
          return item;
        }))
        .type('stacked')
        .id('organization_name')
        .x({ 'value': 'year_month', 'label': 'ماه' })
        .y({ 'value': 'count', 'label': 'تعداد قرارداد' })
        .format({
          "text": function (text, params) {

            if (text === "count") {
              return "تعداد قرارداد";
            }
            else {
              return d3plus.string.title(text, params);
            }

          },
          "number": function (number, params) {
            var formatted = d3plus.number.format(number, params);

            if (params.key === "year_month") {
              let str = number.toString();
              let sp = str.split('.');
              return sp[0].substring(2, 4) + '/' + sp[1] + (sp[1] === '1' ? '0' : '');
            }
            else {
              return formatted;
            }

          }
        })
        .draw();
    }
    $scope.renderOrganizationMonthSum = function () {
      angular.element('#chart').empty();
      $scope.chart = d3plus.viz()
        .container('#chart')
        .data(_.map(_.filter(onOrganizationMonth, i => {
          return i.year >= 1394;
        }), item => {
          item.year_month = Number(item.year + '.' + (item.month < 10 ? '0' : '') + item.month);
          return item;
        }))
        .type('stacked')
        .id('organization_name')
        .x({ 'value': 'year_month', 'label': 'ماه' })
        .y({ 'value': 'sum', 'label': 'مجموع قرارداد' })
        .format({
          "text": function (text, params) {
            if (text === "sum") {
              return "مجموع قرارداد";
            }
            else {
              return d3plus.string.title(text, params);
            }

          },
          "number": function (number, params) {
            var formatted = d3plus.number.format(number, params);

            if (params.key === "year_month") {
              let str = number.toString();
              let sp = str.split('.');
              return sp[0].substring(2, 4) + '/' + sp[1] + (sp[1] === '1' ? '0' : '');
            }
            else {
              return formatted;
            }

          }
        })
        .draw();
    }
    $scope.renderOrganizationYearCount = function () {
      angular.element('#chart').empty();
      $scope.chart = d3plus.viz()
        .container('#chart')
        .data(_.map(_.filter(onOrganizationYear, i => {
          return i.year >= 1394;
        })))
        .type('bar')
        .id('organization_name')
        .x({ 'stacked': true, 'value': 'count', 'label': 'تعداد قرارداد' })
        .y({ 'scale': 'discrete', 'value': 'year', 'label': 'سال' })
        .format({
          "text": function (text, params) {

            if (text === "count") {
              return "تعداد قرارداد";
            }
            else {
              return d3plus.string.title(text, params);
            }

          },
        })
        .draw();
    }
    $scope.renderOrganizationYearSum = function () {
      angular.element('#chart').empty();
      $scope.chart = d3plus.viz()
        .container('#chart')
        .data(_.map(_.filter(onOrganizationYear, i => {
          return i.year >= 1394;
        })))
        .type('bar')
        .id('organization_name')
        .x({ 'stacked': true, 'value': 'sum', 'label': 'مجموع مبلغ قراردادها' })
        .y({ 'scale': 'discrete', 'value': 'year', 'label': 'سال' })
        .format({
          "text": function (text, params) {
            if (text === "sum") {
              return "مجموع قرارداد";
            }
            else {
              return d3plus.string.title(text, params);
            }

          },
        })
        .draw();
    }
    $scope.renderOrganizationMonthCount();
  }

}