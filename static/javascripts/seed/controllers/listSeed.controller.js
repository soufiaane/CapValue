(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'NgTableParams', 'Snackbar', '$state', '$scope', 'ngDialog'];

    function SeedListController(Seed, Authentication, NgTableParams, Snackbar, $state, $scope, ngDialog) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        vm.openSeedDetails = openSeedDetails;
        activate();
        $scope.loading = true;

        Seed.get(user.username).then(function (results) {
            vm.seed_list_count = results.data.length;
            vm.tableParams = new NgTableParams({
                page: 1,
                count: 10
            }, {
                total: results.data.length,
                counts: [],
                data: results.data
            });
            $scope.loading = false;
        }, ErrorSeedListFn);

        function openSeedDetails(seed_id) {
            $scope.detail_loading = true;
            ngDialog.openConfirm({
                template: '/static/templates/seed/seed_detail.html',
                className: 'ngdialog-theme-default custom-width',
                scope: $scope, //Pass the scope object if you need to access in the template
                closeByEscape: true,
                closeByDocument: true,
                preCloseCallback: function () {
                    $scope.selectedSeed = null;
                }
            });
            Seed.get_seed(seed_id).then(function (results) {
                    $scope.detail_loading = false;
                    $scope.selectedSeed = results.data[0];
                },
                function () {
                    $scope.detail_loading = false;
                });
        }

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