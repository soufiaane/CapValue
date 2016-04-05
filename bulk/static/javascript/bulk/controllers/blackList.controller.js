(function () {
    'use strict';

    angular
        .module('capvalue.bulk.controllers')
        .controller('BlackListController', BlackListController);

    BlackListController.$inject = ['Authentication', '$state'];

    function BlackListController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();
