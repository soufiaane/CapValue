(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['Authentication', 'Snackbar'];


    function RegisterController(Authentication) {
        var vm = this;
        activate();
        vm.register = register;

        function register() {
            Authentication.register(vm.password, vm.username);
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                window.location = '/';
            }
        }
    }
})();