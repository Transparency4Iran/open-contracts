import './fonts/IRANSans/WebFonts/css/fontiran.css';
import 'angular-material/angular-material.min.css';
import 'angular-material-data-table/dist/md-data-table.min.css';
import 'adm-dtp/dist/ADM-dateTimePicker.min.css';
import 'bootstrap-v4-rtl/dist/css/bootstrap-rtl.min.css'
import 'bootstrap-v4-rtl/dist/js/bootstrap.bundle.min.js'
import 'animate.css/animate.min.css'
import './styles.scss';
import template from './container.html';

export default class BootstrapComponent {
  constructor() {
    this.template = template;
    this.restrict = 'E';
  }
}
