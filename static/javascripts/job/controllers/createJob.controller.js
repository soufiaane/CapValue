(function () {
        'use strict';
        angular
            .module('capvalue.job.controllers')
            .controller('JobCreateController', JobCreateController);
        JobCreateController.$inject = ['Job'];


    function JobCreateController(Job) {
        var vm = this;

        vm.logg = logg;

        function logg() {
            Job.logg(vm.message);
        }

    }
})();