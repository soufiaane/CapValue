(function () {
    'use strict';

    angular
        .module('capvalue.routes')
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider.state('Register', {
            url: "/register",
            controller: 'RegisterController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/authentication/register.html'
        }).state('Login', {
            url: "/login",
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/authentication/login.html'
        }).state('Home', {
            url: "/",
            controller: 'IndexController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/layout/index.html'
        }).state('Job', {
            url: "/job/create/",
            controller: 'JobController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/job/create.html'
        }).state('JobList', {
            url: "/job/list/",
            controller: 'JobController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/job/list.html'
        }).state('Seed', {
            url: "/seed/create/",
            controller: 'SeedController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/seed/create.html'
        }).state('SeedList', {
            url: "/seed/list/",
            controller: 'SeedController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/seed/list.html'
        });
        $urlRouterProvider.otherwise('/')
    }
})();
