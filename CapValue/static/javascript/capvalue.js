(function () {
    'use strict';

    angular
        .module('capvalue', [
            'capvalue.config',
            'capvalue.routes',
            'capvalue.authentication',
            'capvalue.account',
            'capvalue.layout',
            'capvalue.job',
            'capvalue.seed',
            'capvalue.proxy',
            'capvalue.email',
            'capvalue.utils',
            'capvalue.isp',
            'capvalue.team',
            'capvalue.entity',
            'multiStepForm',
            'ngDialog',
            'ngTable',
            'ngCookies',
            'ui.router',
            'angular-loading-bar'
            //'btford.socket-io'
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
