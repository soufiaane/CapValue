(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobCreateController', JobCreateController);
    JobCreateController.$inject = ['Job', 'Seed', 'Authentication', '$state', 'ngTableParams', 'Snackbar'];

    function JobCreateController(Job, Seed, Authentication, $state, ngTableParams, Snackbar) {
        var vm = this;
        activate();
        vm.job = {
            selectedSeeds: [], actions: [
                {name: "RS", isChecked: true},
                {name: "NS", isChecked: false},
                {name: "RI", isChecked: false},
                {name: "OI", isChecked: false},
                {name: "SS", isChecked: false},
                {name: "AC", isChecked: false},
                {name: "CL", isChecked: false},
                {name: "FM", isChecked: false}
            ]
        };
        var user = Authentication.getAuthenticatedAccount();
        vm.submitJob = submitJob;
        vm.toggleSeedSelection = toggleSeedSelection;
        vm.findWithAttr = findWithAttr;

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

        function findWithAttr(array, attr, value) {
            for (var i = 0; i < array.length; i += 1) {
                if (array[i][attr] === value) {
                    return i;
                }
            }
            return -1;
        }

        function ErrorSeedListFn() {
            console.error('Epic failure!');
        }


        function toggleSeedSelection(seed, seed_id) {
            var idx = findWithAttr(vm.job.selectedSeeds, 'id', seed_id);
            // is currently selected
            if (idx > -1) {
                vm.job.selectedSeeds.splice(idx, 1);
            }
            else {
                vm.job.selectedSeeds.push(JSON.parse(JSON.stringify(seed)));
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

            Job.create(vm.job.keyword, JSON.stringify(vm.job.selectedSeeds), selected_actions).then(createJobSuccessFn, createJobErrorFn);

            function createJobSuccessFn() {
                Snackbar.show('Job Created Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function createJobErrorFn() {
                Snackbar.error('Error when attempting to Create Job');
            }
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }

    }
})();