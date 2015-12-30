(function () {
    'use strict';

    angular
        .module('capvalue.seed.controllers')
        .controller('SeedController', SeedController);

    SeedController.$inject = ['$location', '$scope', 'Seed', 'Authentication', 'FileUpload'];

    function SeedController($location, $scope, Seed, Authentication, FileUpload) {
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
                    download: true,
                    step: function (result) {
                        var progress = result.data[0].indexes;
                        var newPercent = Math.round(progress / size * 100);
                        if (newPercent === percent) return;
                        percent = newPercent;
                        //console.log({percent: percent});
                    },
                    complete: function (results) {
                        vm.parsedData = results;
                    }
                });

            console.log('FINAL RESULT IS: ', vm.parsedData);
        }
    }
})();
