export default class Controller {
  constructor(ContractsService) {
    'ngInject';
    this.service = ContractsService;
  }

  exportExcel() {
    this.service.getContracts({'limit': 100000}).then(resp => {
      this.service.exportExcel(resp.results);
    });

  }

}