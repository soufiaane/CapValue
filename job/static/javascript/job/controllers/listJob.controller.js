(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Authentication', 'NgTableParams', 'Snackbar', '$state', '$scope', 'ngDialog',
        '$interval'];


    function JobListController(Job, Authentication, NgTableParams, Snackbar, $state, $scope, ngDialog, $interval) {
        var vm = this;
        activate();
        var user = Authentication.getAuthenticatedAccount();
        vm.openJobDetails = openJobDetails;
        vm.revokeJob = revokeJob;
        vm.updateJobs = updateJobs;
        vm.deleteJob = deleteJob;
        $scope.loading = true;

        vm.tableParams = new NgTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                var filter = params.filter();
                var sorting = params.sorting();
                var count = params.count();
                return Job.get(user.username, page, filter, sorting, count).then(function (results) {
                    params.total(results.data.count);
                    vm.joblist_count = results.data.count;
                    vm.seed_list_count = results.data.count;
                    params.data = results.data.results;
                    $scope.loading = false;
                    return results.data.results;
                }, ErrorJobListFn);
            },
            counts: []
        });

        //$interval(function () {
        //   vm.updateJobs(vm.tableParams);
        //}, 30000);

        function ErrorJobListFn() {
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

        function revokeJob(celery_id) {
            Job.revoke_job(celery_id).then(SuccessRevokeJobtFn, ErrorRevokeJobtFn);

            function SuccessRevokeJobtFn() {
                Snackbar.show('Job stopped Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function ErrorRevokeJobtFn() {
                Snackbar.error('Error stopping Job !');
            }
        }

        function deleteJob(job_id) {
            Job.delete_Job(job_id).then(SuccessDeleteJobtFn, ErrorDeleteJobtFn);

            function SuccessDeleteJobtFn() {
                Snackbar.show('Job deleted Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function ErrorDeleteJobtFn() {
                Snackbar.error('Error deleting Job !');
            }
        }

        function updateJobs(params) {
            var ignoreLoadingBar = (params.data.length > 0 ) ;
            params.reload();

            Job.updateJobStatus(params.data, ignoreLoadingBar).then(SuccessUpdateJobFn, ErrorUpdateJobFn);

            function SuccessUpdateJobFn() {
                console.log('SuccessUpdateJobFn');
            }

            function ErrorUpdateJobFn() {
                console.log('ErrorUpdateJobFn');
            }
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }

    }
})();
