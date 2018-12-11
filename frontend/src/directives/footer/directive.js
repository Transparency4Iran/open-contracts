import './styles.scss';
import template from './template.html';

export default class FooterComponent {
  constructor() {
    this.template = template;
    this.restrict = 'E';
  }
}