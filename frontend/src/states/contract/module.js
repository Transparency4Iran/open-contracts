import uirouter from 'angular-ui-router';
import mdTable from 'angular-material-data-table';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.contract', [
    uirouter, mdTable
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'contract',
        url: '/contract/{code}',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          contract: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            return ContractsService.getContract($transition$.params().code);
          }],
          distribution: ['ContractsService', function (ContractsService) {
            return ContractsService.getPercentileDistribution();
          }]
        }
      });
    }
  )
;