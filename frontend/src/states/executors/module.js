import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';


export default angular
  .module('omid.states.executors', [
    uirouter
  ])
  .config(function ($stateProvider) {
      'ngInject';

      $stateProvider.state({
        name: 'executors',
        url: '/executors',
        template: Template,
        controller: Controller,
        controllerAs: '$ctrl',
        resolve: {}
      });
    }
  )
;