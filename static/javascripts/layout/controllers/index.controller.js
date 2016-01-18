(function () {
    'use strict';
    angular
        .module('capvalue.layout.controllers')
        .controller('IndexController', IndexController);
    IndexController.$inject = ['Authentication'];
    function IndexController(Authentication) {
        var vm = this;
        vm.isAuthenticated = Authentication.isAuthenticated();
    }
})();