export default function BootstrapConfig ($urlRouterProvider, $locationProvider) {
  'ngInject';

  $locationProvider.html5Mode(true);
  $urlRouterProvider.otherwise('/');
}