(function () {
    'use strict';
    angular
        .module('capvalue.seed.controllers')
        .controller('SeedCreateController', SeedCreateController);
    SeedCreateController.$inject = ['FileUpload'];


    function SeedCreateController() {
        var vm = this;

        vm.steps = [
            {
                templateUrl: '/static/templates/seed/create.info.html',
                title: 'Infos'
            },
            {
                templateUrl: '/static/templates/seed/create.maillist.html',
                title: 'Email List'
            },
            {
                templateUrl: '/static/templates/seed/create.proxy.html',
                title: 'Proxy'
            }
        ];
        vm.master = {};
        vm.seedList = {};
        vm.uploadedFiles = [];
        vm.seedList.emails = {textarea: [], files: []};
        vm.reset = reset;
        vm.checkStep = checkStep;
        vm.checkStep1 = checkStep1;
        vm.checkStep2 = checkStep2;
        vm.checkStep3 = checkStep3;
        vm.seedListInputBind = seedListInputBind;
        vm.uploadFile = uploadFile;


        function seedListInputBind(type) {
            var data;
            var re_email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if ((type == 'file') && vm.selectedFile) {
                vm.uploadedFiles.push(vm.selectedFile);
                vm.selectedFile = null;
            }
            if (vm.seedList.proxyType == "manual") {
                if (type == 'file') {
                    if (vm.selectedFile) {
                        vm.uploadedFiles.push(vm.selectedFile);
                        vm.selectedFile = null;
                    }
                    for (var i = 0; i < vm.uploadedFiles.length; i++) {
                        var file = vm.uploadedFiles[i];
                        var size = file.size;
                        Papa.parse(file,
                            {
                                worker: true,
                                step: function (results) {
                                    var progress = results.indexes[0];
                                    var newPercent = Math.round(progress / size * 100);
                                    if (newPercent === percent) return;
                                    percent = newPercent;
                                },
                                complete: function (results, file) {
                                    //TODO-CVC insert div with file and total seed imported + remove option
                                    var ol = document.createElement("ol");
                                    var li = document.createElement("li");
                                    ol.appendChild(li);
                                    document.getElementById('uploadedFiles').appendChild(ol);
                                }
                            });
                    }
                } else {
                    vm.seedList.emails["textarea"] = [];
                    data = Papa.parse(vm.seedList.textarea_Input).data;
                    for (i = 0; i < data.length; i++) {
                        if (data[i].length == 6) {
                            if (data[i][0] && data[i][1] && re_email.test(data[i][0])) {
                                vm.seedList.emails['textarea'].push({
                                        'email': data[i][0],
                                        'password': data[i][1]
                                    }
                                );
                            }
                            //TODO-CVC Add Proxy Service
                        }
                    }
                }
            } else {
                if (type == 'file') {
                    data = Papa.parse(vm.seedList.textarea_Input).data;
                } else {
                    vm.seedList.emails["textarea"] = [];
                    data = Papa.parse(vm.seedList.textarea_Input).data;
                    for (i = 0; i < data.length; i++) {
                        if (data[i].length == 2) {
                            if (data[i][0] && data[i][1] && re_email.test(data[i][0])) {

                                vm.seedList.emails['textarea'].push({
                                    'email': data[i][0],
                                    'password': data[i][1]
                                });
                            }
                            //TODO-CVC Add Proxy Service
                        }
                    }
                }
            }
        }

        function uploadFile() {
            vm.uploadedFiles.push();
        }

        function reset() {
            vm.user = angular.copy(vm.master);
            //TODO-CVC Goto Step1
        }

        function checkStep($nextStep, $getActiveIndex) {
            var element = document.getElementById("formErrors");
            while (element.firstChild) {
                element.removeChild(element.firstChild);
            }
            if ($getActiveIndex() == '1') {
                checkStep1($nextStep);
            }
            else if ($getActiveIndex() == '2') {
                checkStep2($nextStep);
            }
            else if ($getActiveIndex() == '3') {
                checkStep3($nextStep);
            }
        }

        function checkStep1($nextStep) {
            var errors = [];

            if (!(vm.seedList.name)) {
                errors.push({
                    name: 'seedList.name',
                    error: 'Seed List Name is required !'
                });
            }
            if (!(vm.seedList.proxyType)) {
                errors.push({
                    name: 'seedList.proxyType',
                    error: 'Seed List Proxy Type is required !'
                });
            }
            if (errors.length == 0) {
                $nextStep();
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

                    if (errors[index]['name'] == 'seedList.name') {
                        document.getElementById("seedlist_name").setAttribute("style", errorHighlightStyle);
                    } else if (errors[index]['name'] == 'seedList.proxyType') {
                        document.getElementById("seedlist_proxytype").setAttribute("style", errorHighlightStyle);
                    }
                }
            }
        }

        function checkStep2($nextStep) {
            var errors = [];

            if (!(vm.seedList.name)) {
                errors.push({
                    name: 'seedList.name',
                    error: 'Seed List Name is required !'
                });
            }
            if (!(vm.seedList.proxyType)) {
                errors.push({
                    name: 'seedList.proxyType',
                    error: 'Seed List Proxy Type is required !'
                });
            }
            if (errors.length == 0) {
                $nextStep();
            } else {
                for (var index = 0; index < errors.length; index++) {

                }
            }
        }

        function checkStep3($nextStep) {
            $nextStep();
        }
    }
})();