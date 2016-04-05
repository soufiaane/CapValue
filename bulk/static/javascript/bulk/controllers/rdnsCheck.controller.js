(function () {
    'use strict';

    angular
        .module('capvalue.bulk.controllers')
        .controller('RdnsCheckController', RdnsCheckController);

    RdnsCheckController.$inject = ['Authentication', '$state'];

    function RdnsCheckController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();
