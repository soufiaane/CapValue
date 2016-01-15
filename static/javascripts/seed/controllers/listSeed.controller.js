(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedListController', SeedListController);
    SeedListController.$inject = ['Seed', 'Authentication'];


    function SeedListController(Seed, Authentication) {
        var vm = this;
        var user = Authentication.getAuthenticatedAccount();
        Seed.get(user.username).then(SuccessFn, ErrorFn);

        function SuccessFn(data) {
            vm.seed_list = data.data;
            console.log('SUCCESSSSSSSSSSSSSS!!!');
        }

        function ErrorFn() {
            console.error('Epic failure!');
        }


    }
})();
