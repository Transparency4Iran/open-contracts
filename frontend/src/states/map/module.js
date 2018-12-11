import uirouter from 'angular-ui-router';
import ngmap from 'ngmap';
import mdTable from 'angular-material-data-table';
import mdTableFixedHead from 'angular-fixed-table-header';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.map', [
    uirouter, mdTable, ngmap, mdTableFixedHead
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'map',
        url: '/map',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          topOrganizations: ['ContractsService', function (ContractsService) {
            return ContractsService.getTopOrganizationsWithLeaves();
          }]
        }
      });
    }
  )
;