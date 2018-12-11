import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.organization', [
    uirouter
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'organization',
        url: '/organization/{id}',
        params: {
          id: {value: null}
        },
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          children: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            return ContractsService.getChildren($transition$.params().id);
          }],
          organization: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            if($transition$.params().id) {
              console.log('11');
              return ContractsService.getOrganization($transition$.params().id);
            }
          }],
          contracts: ['ContractsService', '$transition$', function (ContractsService, $transition$) {
            if ($transition$.params().id) {
              console.log('12');
              return ContractsService.getContracts({'organization': $transition$.params().id, 'limit': 100000});
            }
          }]

        }
      });
    }
  )
;