(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobCreateController', JobCreateController);
    JobCreateController.$inject = ['Job', 'Seed', 'Authentication', '$state', 'ngTableParams'];

    function JobCreateController(Job, Seed, Authentication, $state, ngTableParams) {
        var vm = this;
        vm.job = {selectedSeeds: []};
        var user = Authentication.getAuthenticatedAccount();
        Seed.get(user.username).then(Seed_SuccessFn, Seed_ErrorFn);
        vm.job.actions = [
            {name: "RS", isChecked: true},
            {name: "NS", isChecked: false},
            {name: "RI", isChecked: false},
            {name: "OI", isChecked: false},
            {name: "SS", isChecked: false},
            {name: "AC", isChecked: false},
            {name: "CL", isChecked: false},
            {name: "FM", isChecked: false}
        ];
        vm.submitJob = submitJob;
        vm.toggleSeedSelection = toggleSeedSelection;

        function Seed_SuccessFn(results) {
            vm.tableParams = new ngTableParams({page: 1, count: 5}, {data: results.data, counts: []});
        }

        function Seed_ErrorFn() {
            console.error('Epic failure!');
        }

        function toggleSeedSelection(seed) {
            var idx = vm.job.selectedSeeds.indexOf(seed);
            // is currently selected
            if (idx > -1) {
                vm.job.selectedSeeds.splice(idx, 1);
            }
            else {
                vm.job.selectedSeeds.push(seed);
            }
        }

        function submitJob() {
            var selected_actions = "";

            for (var i = 0; i < vm.job.actions.length; i++) {
                if (vm.job.actions[i].isChecked) {
                    selected_actions += vm.job.actions[i].name + ','
                }
            }
            selected_actions = selected_actions.replace(/,\s*$/, "");

            Job.create(vm.job.keyword, vm.job.selectedSeeds, selected_actions).then(createJobSuccessFn, createJobErrorFn);

            function createJobSuccessFn() {
                console.log('Job Created Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function createJobErrorFn() {
                console.error('Error when attempting to Create Job');
            }
        }
    }
})();