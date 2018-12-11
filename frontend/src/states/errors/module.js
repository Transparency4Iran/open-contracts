import uirouter from 'angular-ui-router';
import mdTable from 'angular-material-data-table';
import mdTableFixedHead from 'angular-fixed-table-header';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.errors', [
    uirouter, mdTable, mdTableFixedHead
  ])
  .config(function ($stateProvider) {
    'ngInject';

    $stateProvider.state({
      name: 'errors',
      url: '/errors',
      template: Template,
      controller: Controller,
      controllerAs: '$ctrl',
      resolve: {
        errorSpectrum: ['ContractsService', function (ContractsService) {
          return ContractsService.getByEndpoint('aggregate/error_spectrum');
        }],
        topOrganizations: ['ContractsService', function (ContractsService) {
          return ContractsService.getByEndpoint('top_organizations/statistics');
        }],
        people: ['ContractsService', function (ContractsService) {
          return ContractsService.getByEndpoint('people/statistics/?limit=10000');
        }]
      }
    });
  }
  )
  ;