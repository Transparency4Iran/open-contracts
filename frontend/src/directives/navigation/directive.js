import './styles.scss';
import template from './template.html';

export default class NavigationComponent {
  constructor() {
    this.template = template;
    this.restrict = 'E';
  }
}