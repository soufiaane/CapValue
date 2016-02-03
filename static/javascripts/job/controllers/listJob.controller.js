(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Authentication', 'ngTableParams', 'Snackbar', '$state', '$scope'];


    function JobListController(Job, Authentication, ngTableParams, Snackbar, $state, $scope) {
        var vm = this;
        activate();
        var user = Authentication.getAuthenticatedAccount();
        $scope.loading = true;

        vm.tableParams = new ngTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                return Job.get(user.username).then(function (results) {
                    params.total(results.data.length);
                    vm.joblist_count = results.data.length;
                    $scope.loading = false;
                    console.log('Job List Fetched Successfully !');
                    return results.data;
                }, ErrorSeedListFn);
            },
            counts: []
        });


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
