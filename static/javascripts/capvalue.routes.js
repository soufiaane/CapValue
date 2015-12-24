(function () {
    'use strict';

    angular
        .module('capvalue.routes')
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];


    function config($stateProvider, $urlRouterProvider) {
        $stateProvider.state('home.register', {
            url: "/register",
            controller: 'RegisterController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/authentication/register.html',
            ncyBreadcrumb: {
                label: 'Register'
            }
        }).state('home.login', {
            url: "/login",
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/authentication/login.html',
            ncyBreadcrumb: {
                label: 'Login'
            }
        }).state('home', {
            url: "/",
            controller: 'IndexController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/layout/index.html',
            ncyBreadcrumb: {
                label: 'Home'
            }
        });
        $urlRouterProvider.otherwise("/");
    }
})();