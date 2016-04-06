(function () {
    'use strict';

    angular
        .module('capvalue.account.controllers')
        .controller('ManageAccountsController', ManageAccountsController);

    ManageAccountsController.$inject = ['Account', 'Authentication', '$state', 'NgTableParams', 'Snackbar', '$scope', 'Team'];

    function ManageAccountsController(Account, Authentication, $state, NgTableParams, Snackbar, $scope, Team) {
        var vm = this;
        vm.user = Authentication.getAuthenticatedAccount();
        vm.cancel = cancel;
        activate();

        vm.tableParams = new NgTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                var filter = params.filter();
                var sorting = params.sorting();
                var count = params.count();
                return Account.all(page, filter, sorting, count).then(function (results) {
                    params.total(results.data.count);
                    vm.seed_list_count = results.data.count;
                    for (var i = 0; i < results.data.results.length; i++) {
                        results.data.results[i].role[0] = toTitleCase(results.data.results[i].role[0]);
                    }
                    params.data = results.data.results;
                    $scope.loading = false;
                    return results.data.results;
                }, ErrorSeedListFn);
            },
            counts: []
        });

        vm.roles = [
            {id: 0, title: ''},
            {id: 'mailer', title: 'Mailer'},
            {id: 'team_leader', title: 'Team Leader'},
            {id: 'support', title: 'Support'},
            {id: 'manager', title: 'Manager'}
        ];

        vm.entities = [
            {id: 0, title: ''},
            {id: 1, title: 'CVC1'},
            {id: 2, title: 'CVC2'},
            {id: 3, title: 'CVC3'},
            {id: 4, title: 'Administration'}
        ];

        vm.teams = [];
        Team.all().then(function (results) {
            vm.teams.push({id: 0, title: ''});
            for (var i = 0; i < results.data.results.length; i++) {
                vm.teams.push({
                    id: results.data.results[i].id,
                    title: results.data.results[i].entity[0] + ' -' + results.data.results[i].name
                });
            }
        });

        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Accounts List');
            return [];
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
            if (vm.user.role != 'Manager') {
                $state.go('Home');
            }
            vm.isEditing = false;
        }

        function toTitleCase(str) {
            return str.replace(/\w\S*/g, function (txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
        }

        function cancel() {
            vm.isEditing = false;
        }
    }

})();
