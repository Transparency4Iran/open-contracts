import angular from 'angular';
import 'angular-material';
import 'angular-animate';
import 'angular-aria';
import 'angular-ui-router';
import 'angular-ui-router/lib/legacy/stateEvents';
import app from './app/module';

angular.module('omid', [app]).controller('menuCtrl', function ($scope, $timeout, $mdSidenav) {
  'ngInject';
  $scope.toggleLeft = buildToggler('left');
  $scope.toggleRight = buildToggler('right');

  function buildToggler(componentId) {
    return function () {
      $mdSidenav(componentId).toggle();
    };
  }
});
