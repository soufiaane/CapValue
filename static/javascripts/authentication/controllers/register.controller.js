(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location', '$scope', 'Authentication'];


    function RegisterController($location, $scope, Authentication) {
        var vm = this;
        activate();
        vm.register = register;

        function register() {
            Authentication.register(vm.password, vm.username);
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $location.url('/');
            }
        }
    }
})();