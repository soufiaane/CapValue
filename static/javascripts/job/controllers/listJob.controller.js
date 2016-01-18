(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('JobListController', JobListController);
    JobListController.$inject = ['Job', 'Seed', 'Authentication', 'ngTableParams'];


    function JobListController(Job, Seed, Authentication, ngTableParams) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        Seed.get(user.username).then(SuccessSeedListFn, ErrorSeedListFn);

        function SuccessSeedListFn(results) {
            vm.tableParams = new ngTableParams({page: 1, count: 5}, {data: results.data, counts: []});
            console.log('Seed List Fetched Successfully !');
        }

        function ErrorSeedListFn() {
            console.error('Error fetching Seed List');
            return [];
        }
    }
})();
