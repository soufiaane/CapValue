(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication'];


    function LoginController(Authentication) {
        var vm = this;
        vm.login = login;

        function activate() {
            if (Authentication.isAuthenticated()) {
                window.location = '/';
            }
        }

        function login() {
            Authentication.login(vm.username, vm.password);
        }

        activate();
    }
})();