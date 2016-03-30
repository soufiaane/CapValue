(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'NgTableParams', 'Snackbar', '$state', '$scope', 'ngDialog'];

    function SeedListController(Seed, Authentication, NgTableParams, Snackbar, $state, $scope, ngDialog) {
        var vm = this;
        activate();
        var user = Authentication.getAuthenticatedAccount();
        vm.openSeedDetails = openSeedDetails;
        $scope.loading = true;

        vm.tableParams = new NgTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                return Seed.get(user.username, page).then(function (results) {
                    params.total(results.data.count);
                    vm.seed_list_count = results.data.count;
                    params.data = results.data.results;
                    $scope.loading = false;
                    return results.data.results;
                }, ErrorSeedListFn);
            },
            counts: []
        });

        function openSeedDetails(seed_id) {
            $scope.detail_loading = true;
            ngDialog.openConfirm({
                template: '/static/templates/seed/seed_detail.html',
                className: 'ngdialog-theme-default ng-modal',
                scope: $scope, //Pass the scope object if you need to access in the template
                closeByEscape: true,
                closeByDocument: true,
                preCloseCallback: function () {
                    $scope.selectedSeed = null;
                }
            });

            Seed.get_seed(seed_id).then(function (response) {
                    $scope.detail_loading = false;
                    $scope.selectedSeed = response.data;
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
            vm.isEditing = false;
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();
