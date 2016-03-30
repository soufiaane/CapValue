(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedCreateController', SeedCreateController);
    SeedCreateController.$inject = ['Seed', '$state', 'Snackbar', 'Authentication'];


    function SeedCreateController(Seed, $state, Snackbar, Authentication) {
        var vm = this;
        activate();
        vm.seedList = {emails: {textarea: [], files: []}};
        vm.uploadedFiles = [];
        vm.validate = validate;
        vm.seedListInputBind = seedListInputBind;
        vm.processForm = processForm;
        //*******************************************************************************************************
        function seedListInputBind() {
            var data;
            var re_email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

            vm.seedList.emails["textarea"] = [];
            data = Papa.parse(vm.seedList.textarea_Input).data;
            for (var k = 0; k < data.length; k++) {
                if (data[k][0] && data[k][1] && re_email.test(data[k][0])) {
                    vm.seedList.emails['textarea'].push({
                            'email': data[k][0],
                            'password': data[k][1],
                            'proxy': {
                                'ip': data[k][2] ? data[k][2] : '',
                                'port': data[k][3] ? data[k][3] : '',
                                'login': data[k][4] ? data[k][4] : '',
                                'pass': data[k][5] ? data[k][5] : ''
                            }
                        }
                    );
                }
            }
        }

        function validate() {
            var element = document.getElementById("formErrors");
            var errors = [];
            while (element.firstChild) {
                element.removeChild(element.firstChild);
            }

            if (!(vm.seedList.name)) {
                errors.push({
                    name: 'seedList.name',
                    error: 'Seed List Name is required !'
                });
            }
            if (vm.seedList.emails === {textarea: [], files: []}) {
                errors.push({
                    name: 'seedList.emails',
                    error: 'Email list is empty !'
                });
            }
            if (errors.length === 0) {
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

                    if (errors[index]['name'] === 'seedList.name') {
                        document.getElementById("seedlist_name").setAttribute("style", errorHighlightStyle);
                    } else if (errors[index]['name'] === 'seedList.proxyType') {
                        document.getElementById("seedlist_proxytype").setAttribute("style", errorHighlightStyle);
                    }
                }
                return false;
            }
        }

        function processForm() {
            if (validate() == true) {
                Seed.create(vm.seedList.name, vm.seedList.emails).then(createSeedSuccessFn, createSeedErrorFn);
            }
            function createSeedSuccessFn() {
                Snackbar.show('Seed List Created Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function createSeedErrorFn() {
                Snackbar.error('Error when attempting to Create Seed');
            }
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }
})();