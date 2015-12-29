(function () {
    'use strict';

    angular
        .module('capvalue.seed.controllers')
        .controller('SeedController', SeedController);

    SeedController.$inject = ['$location', '$scope', 'Seed', 'Authentication'];


    function SeedController($location, $scope, Seed, Authentication) {
        var vm = this;

        vm.logg = logg;

        function logg() {
            Seed.logg('Job Controller and Service are working');
        }
    }
})();
(function () {
    'use strict';


    JobController.$inject = ['$location', '$scope', 'Job', 'Authentication'];


    function JobController($location, $scope, Job, Authentication) {
        var vm = this;

        vm.login = logg;

        function logg() {
            Job.logg('Job Controller and Service are working');
        }
    }
})();