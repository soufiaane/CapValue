(function () {
    'use strict';

    angular
        .module('capvalue.seed.controllers')
        .controller('SeedController', SeedController);

    SeedController.$inject = ['$location', '$scope', 'Seed', 'Authentication', 'FileUpload'];

    function SeedController() {
        var vm = this;

        vm.uploadFile = uploadFile;


        vm.seedList = {
            'name': '',
            'proxy_type': '',
            'emails': []
        };
        vm.formData = {};
        vm.parsedData = {};

        // function to process the form
        vm.processForm = processForm;
        vm.seedListInputBind = seedListInputBind;

        function seedListInputBind() {
            var data = Papa.parse(vm.formData.seedList_Input).data;
            vm.seedList.emails = [];
            for (var i = 0; i < data.length; i++) {
                vm.seedList.emails.push({
                    'email': data[i][0],
                    'password': data[i][1]
                });
            }
            //vm.seedList['emails'].push(Papa.parse(vm.formData.seedList_Input).data);
        }

        function processForm() {
            alert('awesome!');
        }

        function uploadFile() {
            var file = vm.myFile;
            var size = file.size;
            var percent = 0;

            var parsedData = vm.parsedData;
            Papa.parse(file,
                {
                    worker: true,
                    step: function (results, parser) {
                        var progress = results.data[0].indexes;
                        console.log(typeof(results.data[0]));
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
    }
})();
