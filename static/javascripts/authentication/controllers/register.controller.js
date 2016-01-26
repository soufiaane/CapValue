(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['Authentication', 'Snackbar'];


    function RegisterController(Authentication, Snackbar) {
        var vm = this;
        activate();
        vm.register = register;

        function register() {
            var fname = vm.fname;
            var lname = vm.lname;
            var username = vm.username;
            var password = vm.password;
            Authentication.register(password, username, fname, lname)
                .then(registerSuccessFn, registerErrorFn);

            function registerSuccessFn(data) {
                Snackbar.show('User Created Successfully !', data);
                Authentication.login(username, password);
            }

            function registerErrorFn() {
                Snackbar.error('Error Creating a new User !');
            }
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                window.location = '/';
            }
        }
    }
})();