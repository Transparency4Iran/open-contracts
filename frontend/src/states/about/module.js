import uirouter from 'angular-ui-router';
import Controller from './controller';
import Template from './template.html';

export default angular
  .module('omid.states.about', [
    uirouter
  ])
  .config(function ($stateProvider) {
    'ngInject';

    $stateProvider.state({
      name: 'about',
      url: '/about',
      template: Template,
      controller: Controller,
      controllerAs: '$ctrl',
      resolve: {
      }
    });
  }
  )
  ;