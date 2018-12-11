import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.executor', [
    uirouter
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'executor',
        url: '/executor/{id}',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          executor: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            return ContractsService.getExecutor($transition$.params().id);
          }],
          contracts: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            return ContractsService.getContracts({'executor': $transition$.params().id, 'limit': 100000});
          }],
          distribution: ['ContractsService', function (ContractsService) {
            return ContractsService.getByEndpoint('aggregate/percentile/executors',false);
          }]

        }
      });
    }
  )
;