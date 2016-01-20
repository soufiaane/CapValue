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
                        Snackbar.show('Seed List Fetched Successfully !', {
                                style: "toast", // add a custom class to your snackbar
                                timeout: 1000, // time in milliseconds after the snackbar autohides, 0 is disabled
                                htmlAllowed: true // allows HTML as content value
                            }
                        );
                        console.log('Seed List Fetched Successfully !');
                        return results.data.results;
                    }, ErrorSeedListFn);
                },
                counts: []
            });


        function ErrorSeedListFn() {
            Snackbar.error('Error fetching Seed List');
            return [];
        }
    }
})();
