export default class Controller {
  constructor(children, organization, contracts) {
    'ngInject';
    this.organization = organization;
    console.log(organization);
    this.contracts = contracts;
    this.children = children;
    this.childrenOrder = 'name';
    this.contractsOrder = '-id';
    d3plus.viz()
      .container('#children')
      .data(_.map(_.sortBy(children, 'implicit_sum').reverse(), function (item) {
        item['مجموع مبلغ قراردادها'] = item.implicit_sum;
        item['سازمان‌های ذیل'] = '';
        return item;
      }))
      .type('bar')
      .id('display_name')
      .y({ 'scale': 'discrete', 'value': 'سازمان‌های ذیل' })
      .x({ 'stacked': true, 'value': 'مجموع مبلغ قراردادها' })
      .height(205)
      // .order('errors_count')
      // .width(1200)
      .draw();
  }
}