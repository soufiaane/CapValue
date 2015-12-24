(function () {
    'use strict';
    angular
        .module('capvalue.layout.controllers')
        .controller('IndexController', IndexController);
    IndexController.$inject = ['$scope', 'Authentication'];
    function IndexController($scope, Authentication) {
        var vm = this;
        vm.isAuthenticated = Authentication.isAuthenticated();
    }
})();