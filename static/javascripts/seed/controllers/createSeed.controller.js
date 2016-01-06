(function () {
    'use strict';

    angular
        .module('capvalue.seed.controllers')
        .controller('SeedCreateController', SeedCreateController);

    SeedCreateController.$inject = [];


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

    }
})();