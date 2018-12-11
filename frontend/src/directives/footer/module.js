import FooterComponent from './directive';
import material from 'angular-material';
export default angular
  .module('omid.directives.footer', [material])
  .directive('omidFooter', () => new FooterComponent());