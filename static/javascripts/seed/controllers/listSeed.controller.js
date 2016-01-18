(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'ngTableParams'];


    function SeedListController(Seed, Authentication, ngTableParams) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        Seed.get(user.username).then(SuccessSeedListFn, ErrorSeedListFn);

        function SuccessSeedListFn(results) {
            vm.tableParams = new ngTableParams({page: 1, count: 5}, {data: results.data, counts: []});
            console.log('');
        }

        function ErrorSeedListFn() {
            console.error('Error fetching Seed List');
            return [];
        }
    }
})();
