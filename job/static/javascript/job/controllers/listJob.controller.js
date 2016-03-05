(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Authentication', 'NgTableParams', 'Snackbar', '$state', '$scope', 'ngDialog'];


    function JobListController(Job, Authentication, NgTableParams, Snackbar, $state, $scope, ngDialog) {
        var vm = this;
        activate();
        var user = Authentication.getAuthenticatedAccount();
        vm.openJobDetails = openJobDetails;
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

        function openJobDetails(job_id) {
            $scope.detail_loading = true;
            var modal = ngDialog.openConfirm({
                template: '/static/templates/job/job_detail.html',
                className: 'ngdialog-theme-default custom-width',
                scope: $scope, //Pass the scope object if you need to access in the template
                closeByEscape: true,
                closeByDocument: true,
                preCloseCallback: function () {
                    $scope.selectedJob = null;
                }
            });
            Job.get_job(job_id).then(function (results) {
                    $scope.detail_loading = false;
                    $scope.selectedJob = results.data[0];
                },
                function () {
                    $scope.detail_loading = false;
                    modal.close();
                });
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();
