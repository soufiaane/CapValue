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
            vm.seedList.emails = {textarea: [], files: []};//{filename: '', emails: []}};
            vm.reset = reset;
            vm.checkStep = checkStep;
            vm.checkStep1 = checkStep1;
            vm.checkStep2 = checkStep2;
            vm.checkStep3 = checkStep3;
            vm.seedListInputBind = seedListInputBind;
            vm.uploadFile = uploadFile;

            //*******************************************************************************************************
            //*******************************************************************************************************
            function seedListInputBind(type) {
                var data;
                var re_email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

                //Handles File Upload & Generating new upload input
                //this is only when we call the function with type == file
                if ((type == 'file') && vm.selectedFile) {
                    vm.uploadedFiles.push(vm.selectedFile);
                    vm.selectedFile = null;
                    document.getElementById("seedfile_import").value = "";
                }
                //*******************************************************************************************************

                //Handles Parsing Logic When proxyType is Manual
                if (vm.seedList.proxyType == "manual") {
                    //*******************************************************************************************************
                    //Handles the File Parsing Logic For Manual ProxyType
                    if (type == 'file') {
                        for (var i = 0; i < vm.uploadedFiles.length; i++) {
                            var imported_data = {filename: vm.uploadedFiles[i].name, emails: []};
                            Papa.parse(vm.uploadedFiles[i],
                                {
                                    step: function (results) {
                                        if (results.data[0][0] && results.data[0][1] && re_email.test(results.data[0][0])) {
                                            imported_data.emails.push({
                                                email: results.data[0][0],
                                                password: results.data[0][1]
                                            });
                                        }
                                    },
                                    complete: function () {
                                        vm.seedList.emails.files.push(imported_data);
                                        checkStep2();
                                    }
                                });
                        }
                    }
                    //******************************************************************************************************

                    //Handles the TextArea Parsing Logic For Manual ProxyType
                    else if (type !== 'file') {
                        vm.seedList.emails["textarea"] = [];
                        data = Papa.parse(vm.seedList.textarea_Input).data;
                        for (var k = 0; k < data.length; k++) {
                            if (data[k].length == 6) {
                                if (data[k][0] && data[k][1] && re_email.test(data[k][0])) {
                                    vm.seedList.emails['textarea'].push({
                                            'email': data[k][0],
                                            'password': data[k][1]
                                        }
                                    );
                                }
                            }
                        }
                    }
                    //******************************************************************************************************

                }
                //******************************************************************************************************

                //Handles Parsing Logic When proxyType is Proxy or VPN
                else if (vm.seedList.proxyType !== "manual") {
                    if (type == 'file') {
                        for (var m = 0; m < vm.uploadedFiles.length; m++) {
                            var imported_data2 = {filename: vm.uploadedFiles[m].name, emails: []};
                            Papa.parse(vm.uploadedFiles[m],
                                {
                                    step: function (results) {
                                        if (results.data[0][0] && results.data[0][1] && re_email.test(results.data[0][0])) {
                                            imported_data2.emails.push({
                                                email: results.data[0][0],
                                                password: results.data[0][1]
                                            });
                                        }
                                    },
                                    complete: function () {
                                        vm.seedList.emails.files.push(imported_data2);
                                        checkStep2();
                                    }
                                });
                        }
                    }
                    else if (type !== 'file') {
                        vm.seedList.emails["textarea"] = [];
                        data = Papa.parse(vm.seedList.textarea_Input).data;
                        for (var l = 0; l < data.length; l++) {
                            if (data[l].length == 2) {
                                if (data[l][0] && data[l][1] && re_email.test(data[l][0])) {

                                    vm.seedList.emails['textarea'].push({
                                        'email': data[l][0],
                                        'password': data[l][1]
                                    });
                                }
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