(function () {
    'use strict';

    angular
        .module('capvalue.job.controllers')
        .controller('JobController', JobController);

    JobController.$inject = ['$location', '$scope', 'Job'];


    function JobController($location, $scope, Job) {
        var vm = this;

        vm.logg = logg;

        function logg() {
            Job.logg(vm.message);
        }
    }
})();