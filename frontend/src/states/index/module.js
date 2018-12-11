import uirouter from 'angular-ui-router';
import mdTable from 'angular-material-data-table';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.index', [
    uirouter, mdTable
  ])
  .config(function ($stateProvider) {
    'ngInject';

    $stateProvider.state({
      name: 'index',
      url: '/',
      template: Template,
      controller: Controller,
      controllerAs: '$ctrl',
      resolve: {
      }
    });
  });
