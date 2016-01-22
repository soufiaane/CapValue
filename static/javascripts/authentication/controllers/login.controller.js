(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication'];


    function LoginController(Authentication) {
        var vm = this;
        vm.login = login;
        activate();


        function activate() {
            // If the user is authenticated, they should not be here.
            if (Authentication.isAuthenticated()) {
                window.location = '/';
            }
        }

        function login() {
            Authentication.login(vm.username, vm.password);
        }
    }
})();