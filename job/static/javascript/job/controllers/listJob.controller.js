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


        vm.tableParams = new NgTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                return Job.get(user.username, page).then(function (results) {
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

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();
