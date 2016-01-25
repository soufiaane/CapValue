(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Authentication', 'ngTableParams', 'Snackbar'];


    function JobListController(Job, Authentication, ngTableParams, Snackbar) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();

        vm.tableParams = new ngTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                return Job.get(user.username, page).then(function (results) {
                    params.total(results.data.count);
                    vm.joblist_count = results.data.count;
                    console.log('Job List Fetched Successfully !');
                    return results.data.results;
                }, ErrorSeedListFn);
            },
            counts: []
        });


        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Job List');
            return [];
        }
    }
})();
