(function () {
    'use strict';

    angular
        .module('capvalue.account.controllers')
        .controller('AccountListController', AccountListController);

    AccountListController.$inject = ['Account', 'Authentication', '$state', 'ngTableParams', 'Snackbar'];

    function AccountListController(Account, Authentication, $state, ngTableParams, Snackbar) {
        var vm = this;
        vm.user = Authentication.getAuthenticatedAccount();
        activate();

        vm.tableParams = new ngTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                var accounts = Account.all(page);
                function a (results) {
                    params.total(results.data.count);
                    vm.account_list_count = results.data.count;
                    console.log('Account List Fetched Successfully !');
                    return results.data.results;
                }
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
    }

})();
