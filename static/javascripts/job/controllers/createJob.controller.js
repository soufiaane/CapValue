(function () {
    'use strict';
    angular
        .module('capvalue.job.controllers')
        .controller('JobCreateController', JobCreateController);
    JobCreateController.$inject = ['Job', 'Seed', 'Authentication', '$state', 'NgTableParams', 'Snackbar', '$scope'];

    function JobCreateController(Job, Seed, Authentication, $state, NgTableParams, Snackbar, $scope) {
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
        $scope.loading = true;
        var user = Authentication.getAuthenticatedAccount();
        vm.submitJob = submitJob;
        vm.toggleSeedSelection = toggleSeedSelection;
        vm.findWithAttr = findWithAttr;
        vm.selected_actions = "";

        Seed.get(user.username).then(function (results) {
            vm.seed_list_count = results.data.length;
            vm.tableParams = new NgTableParams({
                page: 1,
                count: 10
            }, {
                total: results.data.length,
                counts: [],
                data: results.data
            });
            $scope.loading = false;
        }, ErrorSeedListFn);

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
            Snackbar.error('Error fetching Seed List');
            $scope.loading = false;
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

        function isValid() {
            var myNode = document.getElementById("formErrors");
            while (myNode.firstChild) {
                myNode.removeChild(myNode.firstChild);
            }

            var errors = [];
            vm.selected_actions = "";
            for (var i = 0; i < vm.job.actions.length; i++) {
                if (vm.job.actions[i].isChecked) {
                    vm.selected_actions += vm.job.actions[i].name + ','
                }
            }
            vm.selected_actions = vm.selected_actions.replace(/,\s*$/, "");

            if (vm.selected_actions.length < 1) {
                errors.push({
                    name: 'job.actions',
                    error: 'You must select at least 1 action!'
                });
            }

            if (!vm.job.keyword) {
                errors.push({
                    name: 'job.keyword',
                    error: 'You must Enter a keyword!'
                });
            }

            if (vm.job.selectedSeeds.length < 1) {
                errors.push({
                    name: 'job.selectedSeeds',
                    error: 'You must select at least 1 Seed List!'
                });
            }

            if (errors.length == 0) {
                return true;
            } else {
                for (var index = 0; index < errors.length; index++) {
                    var errorHighlightStyle = "border-color: #dd4b39;border-style: solid; box-shadow: 0 0 8px #DD4B39;";
                    var div = document.createElement("div");
                    div.setAttribute("class", "callout callout-danger");
                    div.setAttribute("style", "padding: 1px 30px 1px 15px; margin-top: 2px;");
                    var h4 = document.createElement("h4");
                    h4.innerHTML = errors[index]['error'];
                    div.appendChild(h4);
                    document.getElementById("formErrors").appendChild(div);

                    if (errors[index]['name'] == 'job.actions') {
                        document.getElementById("job_actions").setAttribute("style", errorHighlightStyle);
                    } else if (errors[index]['name'] == 'job.keyword') {
                        document.getElementById("job_keyword").setAttribute("style", errorHighlightStyle);
                    }else if (errors[index]['name'] == 'job.selectedSeeds') {
                        document.getElementById("job_seed_list").setAttribute("style", errorHighlightStyle);
                    }
                }
                return false;
            }
        }

        function submitJob() {
            if (isValid()) {
                Job.create(vm.job.keyword, JSON.stringify(vm.job.selectedSeeds), vm.selected_actions).then(createJobSuccessFn, createJobErrorFn);
            }

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