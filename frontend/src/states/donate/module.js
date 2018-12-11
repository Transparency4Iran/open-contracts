import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.donate', [
    uirouter
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'donate',
        url: '/donate',
        template: Template,
        controller: Controller,
        // controllerAs: '$ctrl',
        resolve: {
        }
      });
    }
  )
;