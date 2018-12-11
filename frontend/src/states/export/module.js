import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.export', [
    uirouter
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'export',
        url: '/export',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {
        }
      });
    }
  )
;