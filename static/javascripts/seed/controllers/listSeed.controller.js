(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'ngTableParams', 'Snackbar', '$state', '$scope'];

    function SeedListController(Seed, Authentication, ngTableParams, Snackbar, $state, $scope) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        activate();
        $scope.loading = true;

        vm.tableParams = new ngTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                return Seed.get(user.username).then(function (results) {
                    vm.seed_list_count = results.data.length;
                    params.total(results.data.length);
                    $scope.loading = false;
                    console.log('Seed List Fetched Successfully !');
                    return results.data;
                }, ErrorSeedListFn)
            },
            counts: []
        });

        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Seed List');
            $scope.loading = false;
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();

//dataset: data