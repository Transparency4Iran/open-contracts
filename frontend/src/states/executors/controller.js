export default class Controller {
  constructor(ContractsService) {
    'ngInject';
    this.service = ContractsService;
    this.query = {
      ordering: '-sum',
      page: 1,
      limit: 20,
      name__contains: ''
    };
    let $ctrl = this;
    this.change = function () {
      if ($ctrl.query.page > 1) {
        $ctrl.query.offset = ($ctrl.query.page - 1) * $ctrl.query.limit;
      }
      $ctrl.promise = $ctrl.service.getExecutorsList($ctrl.query).then(resp => {
        $ctrl.resp = resp;
      });
    };
    this.change();
  }


}