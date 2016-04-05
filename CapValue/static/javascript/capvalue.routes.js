(function () {
    'use strict';

    angular
        .module('capvalue.routes')
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('Home', {
                url: "/",
                controller: 'IndexController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/home.html'
            })
            .state('Login', {
                url: "/login",
                controller: 'LoginController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/authentication/login.html'
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
                controller: 'JobListController',
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
            })
            .state('AccountsList', {
                url: "/accounts/list/",
                controller: 'AccountListController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/account/list.html'
            })
            .state('BlackListCheck', {
                url: "/bulk/blcheck/",
                controller: 'BlackListController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/bulk/dnsbl.html'
            })
            .state('SpfCheck', {
                url: "/bulk/spf/",
                controller: 'SpfCheckController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/bulk/spf.html'
            })
            .state('RdnsCheck', {
                url: "/bulk/rdns/",
                controller: 'RdnsCheckController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/bulk/rdns.html'
            })
            .state('FindSubject', {
                url: "/bulk/find_subject/",
                controller: 'FindSubjectController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/bulk/find_subject.html'
            })
            .state('IpNeghbours', {
                url: "/bulk/ip_neghbours/",
                controller: 'IpNeghboursController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/bulk/ip_neghbours.html'
            })
            .state('usersAdmin', {
                url: "/admin/users/",
                controller: 'ManageAccountsController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/authentication/users.html'
            });
        $urlRouterProvider.otherwise('/')
    }
})();
