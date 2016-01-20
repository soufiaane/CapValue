(function () {
    'use strict';
    angular
        .module('capvalue.layout.controllers')
        .controller('IndexController', IndexController);
    IndexController.$inject = ['$scope', 'Authentication', 'Snackbar'];
    function IndexController($scope, Authentication, Snackbar) {
        var vm = this;
        vm.isAuthenticated = Authentication.isAuthenticated();
    }
})();