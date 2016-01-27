(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['Authentication', 'Snackbar', 'ISP', '$rootScope', '$scope', 'Team'];


    function RegisterController(Authentication, Snackbar, ISP, $rootScope, $scope, Team) {
        var vm = this;
        vm.isps = [];
        vm.teams = [];
        vm.selected_isp = "";
        vm.selected_team = "";
        ISP.all().then(function (results) {
            vm.isps = results.data;
        });
        vm.ISPSelected = ISPSelected;
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

        function ISPSelected() {
            Team.get_team_isp(vm.selected_isp).then(function (results) {
                vm.teams = results.data;

                $rootScope.isp_teams = {
                    show: true
                };
                $scope.isp_teams = $rootScope.isp_teams;
            });
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $rootScope.isp_teams.show = false;
                window.location = '/';
            }
        }
    }
})();