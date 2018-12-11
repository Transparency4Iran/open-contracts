export default class Controller {
  constructor(errorSpectrum, topOrganizations, people) {
    'ngInject';
    angular.element('#errorContract a').on('click', function (e) {
      e.preventDefault()
      angular.element('#errorContract .nav-link').removeClass('active')
      angular.element('#errorContract .nav-item').removeClass('active')
      angular.element(this).addClass('active')
      var newTab = angular.element(this).attr('href')
      angular.element('.tab-content .tab-pane').removeClass('active')
      angular.element('.tab-content .tab-pane').addClass('fade')
      angular.element(newTab).addClass('active')
      angular.element(newTab).removeClass('fade')
    })

    this.topOrganizations = _.map(topOrganizations, item => {
      item.percent = 100 * item.errors_count / item.contracts_count;
      return item;
    });
    this.people = _.map(people, item => {
      item.percent = 100 * item.errors_count / item.contracts_count;
      return item;
    });
    this.topOrganizationOrder = '-percent';
    this.peopleOrder = '-percent';
    d3plus.viz()
      .container('#errorSpectrum')
      .data(_.map(errorSpectrum, function (item) {
        item['تعداد قرارداد'] = item.count;
        item['خطا'] = item.label;
        return item;
      }))
      .type('bar')
      .id('label')
      .y({
        'value': 'تعداد قرارداد'
      })
      .x({
        'scale': 'discrete',
        'value': 'خطا'
      })
      .order('count')
      .height(400)
      .draw();
    d3plus.viz()
      .container('#topOrganizations')
      .data(_.map(_.sortBy(topOrganizations, 'errors_count').reverse(), function (item) {
        item['تعداد خطا'] = item.errors_count;
        item['پخش خطا در کارفرمایان'] = '';
        return item;
      }))
      .type('bar')
      .id('display_name')
      .y({
        'scale': 'discrete',
        'value': 'پخش خطا در کارفرمایان'
      })
      .x({
        'stacked': true,
        'value': 'تعداد خطا'
      })
      .height(205)
      // .order('errors_count')
      // .width(1200)
      .draw();
  }

}