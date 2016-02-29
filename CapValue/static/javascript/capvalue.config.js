(function () {
    'use strict';

    angular
        .module('capvalue.config')
        .config(config);

    config.$inject = ['$locationProvider', '$interpolateProvider', '$httpProvider'];


    function config($locationProvider, $interpolateProvider, $httpProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }
})();