import moment from 'moment-jalaali';
import XLSX from 'xlsx';
import FileSaver from 'file-saver';

export default class ContractsService {
  constructor($http) {
    'ngInject';
    this.$http = $http;
    this.base = 'https://api.cdb.tp4.ir/';
    // this.base = 'http://localhost:8000/';
  }

  objectToQueryString(obj) {
    let str = [];

    for (var p in obj) {
      if (obj.hasOwnProperty(p) && obj[p] !== undefined && obj[p] !== null && obj[p] !== '') {
        let property = encodeURIComponent(p);
        if (property.endsWith('__ne')) {
          property = property.substring(0, property.length - 4);
          str.push(property + '!=' + encodeURIComponent(obj[p]));
        } else {
          str.push(property + '=' + encodeURIComponent(obj[p]));
        }
      }
    }
    return str.join('&');
  }

  getContracts(query, results = false) {
    return this.$http.get(this.base + 'contracts/?' + this.objectToQueryString(query)).then(resp => {
      if (results) {
        return resp.data.results;
      }
      return resp.data;
    });
  }

  getExecutorsList(query, results = false) {
    return this.$http.get(this.base + 'executors/?' + this.objectToQueryString(query)).then(resp => {
      if (results) {
        return resp.data.results;
      }
      return resp.data;
    });
  }

  getTopOrganizationsWithLeaves() {
    return this.$http.get(this.base + 'top_organizations/').then(resp => {
      return _.map(resp.data.results, item => {
        item.leaves = _.map(item.leaves, leaf => {
          leaf.id = leaf.path[leaf.path.length - 1].id;
          leaf.path.shift();
          leaf.displayPath = _.pluck(leaf.path, 'display_name').join('/');
          return leaf;
        });
        return item;
      });
    });
  }

  getContract(code) {
    return this.$http.get(this.base + 'contracts/' + code + '/').then(resp => {
      return resp.data;
    });
  }

  getByEndpoint(path, results = true) {
    return this.$http.get(this.base + path).then(resp => {
      if (results) {
        return resp.data.results;
      }
      return resp.data;
    });
  }
  getPromiseByEndpoint(path) {
    return this.$http.get(this.base + path)
  }



  getCategories() {
    return this.getByEndpoint('categories/?limit=100000');
  }

  getCreditSources() {
    return this.getByEndpoint('credit_sources/?limit=100000');
  }

  getGeneralRules() {
    return this.getByEndpoint('general_rules/?limit=100000');
  }

  // getExecutors() {
  //   return this.getByEndpoint('executors/summary/?limit=100000');
  // }

  getProvinces() {
    return this.getByEndpoint('provinces/?limit=100000');
  }


  getOnOrganizationYearAggregation() {
    return this.getByEndpoint('aggregate/top_organization/year/?limit=100000');
  }

  getOnOrganizationMonthAggregation() {
    return this.getByEndpoint('aggregate/top_organization/month/?limit=100000');
  }

  getOnLocation(scale, query = {}) {
    return this.getByEndpoint('aggregate/' + scale + '/?' + this.objectToQueryString(query));
  }

  getPercentileDistribution() {
    return this.getByEndpoint('aggregate/percentile/?limit=100000', false);
  }

  exportExcel(list) {

    /* generate a worksheet */
    var ws = XLSX.utils.json_to_sheet(_.map(list, item => {
      item.town = (item.city === null ? '' : item.city.town);
      item.province = (item.city === null ? '' : item.city.province);
      item.city = (item.city === null ? '' : item.city.name);
      item.organizations = _.pluck(item.organizations, 'display_name').join('/');
      item.registrar = item.registrar.display_name;
      item.executor = (item.executor === null ? '' : item.executor.name);
      delete item['$$hashKey'];
      return item;
    }));

    /* add to workbook */
    var wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Contracts");

    /* write workbook (use type 'binary') */
    var wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });

    /* generate a download */
    function s2ab(s) {
      var buf = new ArrayBuffer(s.length);
      var view = new Uint8Array(buf);
      for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
      return buf;
    }

    FileSaver.saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), "contracts.xlsx");
  }

  getChildren(id = null) {
    return this.getByEndpoint('organizations/?limit=10000&father' + (id === null ? '__isnull=true' : '=' + id));
  }

  getOrganization(id) {
    return this.getByEndpoint('organizations/' + id + '/', false);
  }

  getExecutor(id) {
    return this.getByEndpoint('executors/' + id + '/', false);
  }

  getDailyFetchPerTopOrganization(days) {
    let start_date = moment().subtract(days, 'day').format('YYYY-MM-DD');
    return this.getPromiseByEndpoint('aggregate/daily_fetch_per_top_organization?limit=10000&date__gte=' + start_date);
  }
}
