(function () {
    'use strict';

    angular
        .module('capvalue', [
            'capvalue.config',
            'capvalue.routes',
            'capvalue.authentication',
            'capvalue.layout',
            'capvalue.job',
            'capvalue.seed',
            'capvalue.proxies',
            'capvalue.emails',
            'capvalue.utils',
            'ncy-angular-breadcrumb',
            'multiStepForm',
            'ngTable',
            'ngCookies',
            'ui.router'
        ]).run(run);

    run.$inject = ['$http'];
    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }

    angular
        .module('capvalue.routes', ['ui.router']);
    angular
        .module('capvalue.config', []);
})();
