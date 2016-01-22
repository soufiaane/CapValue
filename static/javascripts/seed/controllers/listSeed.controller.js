(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication', 'ngTableParams', 'Snackbar'];

    function SeedListController(Seed, Authentication, ngTableParams, Snackbar) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();

        vm.tableParams = new ngTableParams({
            page: 1,
            count: 10
        }, {
            getData: function (params) {
                var page = params.page();
                return Seed.get(user.username, page).then(function (results) {
                    params.total(results.data.count);
                    vm.seed_list_count = results.data.count;
                    console.log('Seed List Fetched Successfully !');
                    return results.data.results;
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
