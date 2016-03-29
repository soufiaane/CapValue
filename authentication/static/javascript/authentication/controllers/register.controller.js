(function () {
    'use strict';

    angular
        .module('capvalue.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['Authentication', 'Snackbar', '$rootScope', '$scope', 'Entity'];


    function RegisterController(Authentication, Snackbar, $rootScope, $scope, Entity) {
        var vm = this;
        vm.entities = [];
        vm.teams = [];
        vm.selected_entity = "";
        vm.selected_team = "";
        Entity.all().then(function (response) {
            vm.entities = response.data.results;
        });
        vm.ENTITYSelected = ENTITYSelected;
        activate();
        vm.register = register;

        function register() {
            var fname = vm.fname;
            var lname = vm.lname;
            var selected_team = vm.selected_team;
            var username = vm.username;
            var password = vm.password;
            Authentication.register(password, username, fname, lname, selected_team)
                .then(registerSuccessFn, registerErrorFn);

            function registerSuccessFn(data) {
                Snackbar.show('User Created Successfully !', data);
                Authentication.login(username, password);
            }

            function registerErrorFn() {
                Snackbar.error('Error Creating a new User !');
            }
        }

        function ENTITYSelected() {
            Entity.get_teams(vm.selected_entity).then(function (results) {
                vm.teams = results.data;

                $rootScope.entity_teams = {
                    show: true
                };
                $scope.entity_teams = $rootScope.entity_teams;
            });
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $rootScope.entity_teams.show = false;
                window.location = '/';
            }
        }
    }
})();