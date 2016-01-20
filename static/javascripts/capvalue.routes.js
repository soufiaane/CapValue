(function () {
    'use strict';

    angular
        .module('capvalue.routes')
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider.state('Home', {
                url: "/",
                controller: 'IndexController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/layout/index.html'
            })
            .state('Register', {
                url: "/register",
                controller: 'RegisterController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/authentication/register.html'
            })
            .state('JobCreate', {
                url: "/job/create/",
                controller: 'JobCreateController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/job/create.html'
            })
            .state('JobList', {
                url: "/job/list/",
                controller: 'JobCreateController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/job/list.html'
            })
            .state('SeedList', {
                url: "/seed/list/",
                controller: 'SeedListController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/seed/list.html'
            })
            .state('SeedCreate', {
                url: "/seed/create/",
                controller: 'SeedCreateController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/seed/create.html'
            });
        $urlRouterProvider.otherwise('/')
    }
})();
