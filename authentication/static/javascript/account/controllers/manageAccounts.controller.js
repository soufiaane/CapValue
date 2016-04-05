(function () {
    'use strict';

    angular
        .module('capvalue.account.controllers')
        .controller('ManageAccountsController', ManageAccountsController);

    ManageAccountsController.$inject = ['Account', 'Authentication', '$state', 'NgTableParams', 'Snackbar', '$scope'];

    function ManageAccountsController(Account, Authentication, $state, NgTableParams, Snackbar, $scope) {
        var vm = this;
        vm.user = Authentication.getAuthenticatedAccount();
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
        }

        function toTitleCase(str) {
            return str.replace(/\w\S*/g, function (txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
        }
    }

})();
