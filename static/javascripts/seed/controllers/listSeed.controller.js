(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'ngTableParams', 'Snackbar', '$state', '$scope', 'ngDialog'];

    function SeedListController(Seed, Authentication, ngTableParams, Snackbar, $state, $scope, ngDialog) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        vm.openSeedDetails = openSeedDetails;
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
                    return results.data;
                }, ErrorSeedListFn)
            },
            counts: []
        });

        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Seed List');
            $scope.loading = false;
        }


        function openSeedDetails(seed_id) {
            console.log(seed_id);
            ngDialog.open({
                template:'\
                <p>Are you sure you want to close the parent dialog?</p>\
                <div class="ngdialog-buttons">\
                    <button type="button" class="ngdialog-button ngdialog-button-secondary" ng-click="closeThisDialog(0)">No</button>\
                    <button type="button" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(1)">Yes</button>\
                </div>',
                plain: true
            });
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();

//dataset: data