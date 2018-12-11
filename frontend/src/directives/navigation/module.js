import NavigationComponent from './directive';
import material from 'angular-material';
export default angular
  .module('omid.directives.navigation', [material])
  .directive('omidNavigation', () => new NavigationComponent());