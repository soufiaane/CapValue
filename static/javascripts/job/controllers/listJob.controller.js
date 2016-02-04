(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Authentication', 'NgTableParams', 'Snackbar', '$state', '$scope'];


    function JobListController(Job, Authentication, NgTableParams, Snackbar, $state, $scope) {
        var vm = this;
        activate();
        var user = Authentication.getAuthenticatedAccount();
        $scope.loading = true;

        Job.get(user.username).then(function (results) {
            vm.joblist_count = results.data.length;
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

        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Job List');
            $scope.loading = false;
            return [];
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();
