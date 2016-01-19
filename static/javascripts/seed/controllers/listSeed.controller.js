(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'ngTableParams'];

    function SeedListController(Seed, Authentication, ngTableParams) {
        var vm = this;

        vm.tableParams = new ngTableParams({
                page: 1,
                count: 10
            },
            {
                getData: function (params) {
                    return Seed.get(Authentication.getAuthenticatedAccount().username).then(function (results) {
                        params.total(results.data.length);
                        console.log('Seed List Fetched Successfully !');
                        return results.data;
                    }, ErrorSeedListFn);
                },
                counts: []
            });


        function ErrorSeedListFn() {
            console.error('Error fetching Seed List');
            return [];
        }
    }
})();
