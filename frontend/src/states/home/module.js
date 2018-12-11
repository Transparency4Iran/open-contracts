import uirouter from 'angular-ui-router';
import mdTable from 'angular-material-data-table';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.home', [
    uirouter, mdTable
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'home',
        url: '/statistics',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          onOrganizationYear: ['ContractsService', function (ContractsService) {
            return ContractsService.getOnOrganizationYearAggregation();
          }],
          onOrganizationMonth: ['ContractsService', function (ContractsService) {
            return ContractsService.getOnOrganizationMonthAggregation();
          }]
        }
      });
    }
  )
;