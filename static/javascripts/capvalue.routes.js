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
            })
            .state('Login', {
                url: "/login",
                controller: 'LoginController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/authentication/login.html'
            })
            .state('Home', {
                url: "/",
                controller: 'IndexController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/layout/index.html'
            })
            .state('Job', {
                url: "/job/create/",
                controller: 'JobController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/job/create.html'
            })
            .state('JobList', {
                url: "/job/list/",
                controller: 'JobController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/job/list.html'
            })
            .state('SeedList', {
                url: "/seed/list/",
                controller: 'SeedController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/seed/list.html'
            })
            .state('SeedCreate', {
                url: "/seed/create/",
                controller: 'SeedController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/seed/create.html'
            })
            .state('SeedCreate.info', {
                url: '/seed/create/info/',
                templateUrl: '/static/templates/seed/form-info.html'
            })

            // url will be /form/interests
            .state('SeedCreate.maillist', {
                url: '/seed/create/maillist/',
                templateUrl: '/static/templates/seed/form-maillist.html'
            })

            // url will be /form/payment
            .state('SeedCreate.proxy', {
                url: '/seed/create/proxy',
                templateUrl: '/static/templates/seed/form-proxy.html'
            });
        $urlRouterProvider.otherwise('/')
    }
})();
