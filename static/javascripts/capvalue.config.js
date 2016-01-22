(function () {
    'use strict';

    angular
        .module('capvalue.config')
        .config(config);

    config.$inject = ['$locationProvider', '$interpolateProvider'];


    function config($locationProvider, $interpolateProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }
})();