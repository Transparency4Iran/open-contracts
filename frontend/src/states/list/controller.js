import moment from 'moment-jalaali';
import JSURL from 'jsurl';

export default class Controller {
  constructor(categories, creditSources, generalRules, provinces, topOrganizations, people, query, ContractsService, clipboard, $mdToast, $scope, $rootScope, $state) {
    'ngInject';
    $scope.registrars = people;
    $scope.categories = categories;
    $scope.creditSources = creditSources;
    $scope.generalRules = generalRules;
    $scope.provinces = provinces;
    $scope.topOrganizations = topOrganizations;
    $scope.service = ContractsService;
    $scope.clipboard = clipboard;
    $scope.DEFAULT_LIMIT = 10;
    $scope.DEFAULT_ORDERING = '-id';
    $scope.allErrors = [
      'خطای مفهومی ثبت شده توسط دبیر',
      'تاریخ انعقاد در آینده',
      'فیلد خالی مهلت',
      'ثبت نادرست مهلت',
      'مهلت زودتر از انعقاد',
      'فیلد خالی مکان',
      'فیلد خالی قیمت',
      'فیلد خالی مجری'
    ];
    $scope.selectedErrors = [];
    //rebuild query object and ui state based on url
    if (!query) {
      query = '~()';
    }
    $scope.query = JSURL.parse(query);
    if (!$scope.query.limit) {
      $scope.query.limit = $scope.DEFAULT_LIMIT;
    }
    if (!$scope.query.ordering) {
      $scope.query.ordering = $scope.DEFAULT_ORDERING;
    }
    if (!$scope.query.page) {
      $scope.query.page = 1;
    }
    if ($scope.query.offset) {
      $scope.query.page = $scope.query.offset / $scope.query.limit + 1;
    }
    if ($scope.query.contract_date__gte) {
      $scope.start_contract_date = moment($scope.query.contract_date__gte, 'YYYY-MM-DD').format('jYYYY/jM/jD');
    }
    if ($scope.query.contract_date__lte) {
      $scope.end_contract_date = moment($scope.query.contract_date__lte, 'YYYY-MM-DD').format('jYYYY/jM/jD');
    }
    if ($scope.query.end_date__gte) {
      $scope.start_end_date = moment($scope.query.end_date__gte, 'YYYY-MM-DD').format('jYYYY/jM/jD');
    }
    if ($scope.query.end_date__lte) {
      $scope.end_end_date = moment($scope.query.end_date__lte, 'YYYY-MM-DD').format('jYYYY/jM/jD');
    }
    if ($scope.query.errors__ne !== undefined) {
      $scope.errorStatus = 'nok';
    } else if ($scope.query.errors === 0) {
      $scope.errorStatus = 'ok';
    } else if ($scope.query.errors === undefined) {
      $scope.errorStatus = 'all';
    } else {
      $scope.errorStatus = 'select';
      let n = Number(angular.copy($scope.query.errors));
      for (let i = 0; i < $scope.allErrors.length; i++) {
        if ((n % 2) === 1) {
          $scope.selectedErrors.push(i.toString());
        }
        n = Math.floor(n / 2);
      }
    }
    if ($scope.query.city__town__province__id) {
      $scope.towns = _.findWhere($scope.provinces, {
        'id': $scope.query.city__town__province__id
      }).towns;
    }
    if ($scope.query.city__town) {
      $scope.cities = _.findWhere($scope.towns, {
        'id': $scope.query.city__town
      }).cities;
    }
    if ($scope.query.top_organization) {
      $scope.leaves = _.findWhere($scope.topOrganizations, {
        'id': $scope.query.top_organization
      }).leaves;
    }


    //turn ui state to query object
    $scope.cleanQuery = function () {
      if ($scope.start_contract_date) {
        $scope.query.contract_date__gte = moment($scope.start_contract_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      if ($scope.end_contract_date) {
        $scope.query.contract_date__lte = moment($scope.end_contract_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      if ($scope.start_end_date) {
        $scope.query.end_date__gte = moment($scope.start_end_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      if ($scope.end_end_date) {
        $scope.query.end_date__lte = moment($scope.end_end_date, 'jYYYY/jM/jD').format('YYYY-MM-DD');
      }
      if ($scope.query.page > 1) {
        $scope.query.offset = ($scope.query.page - 1) * $scope.query.limit;
      }
      if ($scope.errorStatus === 'all') {
        delete $scope.query.errors__ne;
        delete $scope.query.errors;
      } else if ($scope.errorStatus === 'ok') {
        $scope.query.errors = 0;
        delete $scope.query.errors__ne;
      } else if ($scope.errorStatus === 'nok') {
        $scope.query.errors__ne = 0;
        delete $scope.query.errors;
      } else {
        delete $scope.query.errors__ne;
        if ($scope.selectedErrors.length > 0) {
          $scope.query.errors = 0;
          for (let error of $scope.selectedErrors) {
            console.log(error);
            $scope.query.errors += Math.pow(2, Number(error));
          }
        }
      }
    };
    $scope.codeUrl = function () {
      let query = JSON.parse(JSON.stringify($scope.query));
      if (query.page === 1) {
        delete query.page;
      }
      if (query.ordering === $scope.DEFAULT_ORDERING) {
        delete query.ordering;
      }
      if (query.limit === $scope.DEFAULT_LIMIT) {
        delete query.limit;
      }
      if (!query.executor__name__contains) {
        delete query.executor__name__contains;
      }
      let coded = JSURL.stringify(query);
      if (coded.length < 7) {
        coded = null;
      }
      return coded;
    };
    $scope.change = function () {
      $scope.cleanQuery();
      $scope.promise = $scope.service.getContracts($scope.query).then(resp => {
        $scope.resp = resp;
      });
      $state.go('list', {
        query: $scope.codeUrl()
      });
      $rootScope.loading = false;
    };
    $scope.change();

    $scope.copyURL = function () {
      $scope.cleanQuery();
      $scope.clipboard.copyText('http://contracts.odpo.ir/list/' + $scope.codeUrl());
      $mdToast.show(
        $mdToast.simple()
          .textContent('لینک کپی شد')
          .position('top right')
          .hideDelay(3000)
      );
    };
    $scope.exportExcel = function () {
      $scope.service.exportExcel($scope.resp.results);
    };

    $scope.changeProvince = function () {
      const province_id = $scope.query.city__town__province__id;
      if (province_id) {
        $scope.towns = _.findWhere($scope.provinces, {
          'id': province_id
        }).towns;
      } else {
        $scope.towns = false;
      }
      $scope.cities = false;
      $scope.query.city__town = '';
      $scope.query.city = '';
    };

    $scope.changeTown = function () {
      const town_id = $scope.query.city__town;
      if (town_id) {
        $scope.cities = _.findWhere($scope.towns, {
          'id': town_id
        }).cities;
      } else {
        $scope.cities = false;
      }
      $scope.query.city = '';

    };

    $scope.changeTopOrganization = function () {
      const top_id = $scope.query.top_organization;
      if (top_id) {
        $scope.leaves = _.findWhere($scope.topOrganizations, {
          'id': top_id
        }).leaves;
      } else {
        $scope.leaves = false;
      }
      $scope.query.organization = '';

    };

    $scope.searchForExecutors = function (searchText) {
      return $scope.service.getByEndpoint('executors/?name__contains=' + searchText);
    };

  }
}