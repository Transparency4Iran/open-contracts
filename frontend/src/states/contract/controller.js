import moment from 'moment-jalaali'

export default class Controller {
  constructor(contract, distribution, $rootScope) {
    'ngInject';
    this.contract = contract;
    $rootScope.percentile(distribution, contract.price);
    this.contract.delay = moment(contract.fetch_date).diff(moment(contract.contract_date), 'days');
  }

}