import uirouter from 'angular-ui-router';
import material from 'angular-material';
import mdTable from 'angular-material-data-table';
import mdTableFixedHead from 'angular-fixed-table-header';
import Controller from './controller';
import Template from './template.html';
import 'moment-jalaali';
import 'adm-dtp/dist/ADM-dateTimePicker.min';
import 'adm-dtp/dist/ADM-dateTimePicker.min.css';
import clipboardModule from 'angular-clipboard/angular-clipboard';

export default angular
  .module('omid.states.list', [
    uirouter, material, mdTable, mdTableFixedHead, 'ADM-dateTimePicker',clipboardModule.name
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'list',
        url: '/list/{query}',
        params: {
          query: {value: null,dynamic:true}
        },
        reloadOnSearch : false,
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
          categories: ['ContractsService', function (ContractsService) {
            return ContractsService.getCategories();
          }],
          creditSources: ['ContractsService', function (ContractsService) {
            return ContractsService.getCreditSources();
          }],
          generalRules: ['ContractsService', function (ContractsService) {
            return ContractsService.getGeneralRules();
          }],
          provinces: ['ContractsService', function (ContractsService) {
            return ContractsService.getProvinces();
          }],
          topOrganizations: ['ContractsService', function (ContractsService) {
            return ContractsService.getTopOrganizationsWithLeaves();
          }],
          people: ['ContractsService', function (ContractsService) {
            return ContractsService.getByEndpoint('people');
          }],
          query: ['$transition$', function ($transition$) {
            return $transition$.params().query;
          }]
        }
      });
    }
  )
;