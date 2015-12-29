(function () {
    'use strict';

    angular
        .module('capvalue.seed.controllers')
        .controller('SeedController', SeedController);

    SeedController.$inject = ['$location', '$scope', 'Seed', 'Authentication'];


    function SeedController($location, $scope, Seed, Authentication) {
        var vm = this;

        vm.formData = {};

        // function to process the form
        vm.processForm = processForm;

        function processForm() {
            alert('awesome!');
        }
    }
})();