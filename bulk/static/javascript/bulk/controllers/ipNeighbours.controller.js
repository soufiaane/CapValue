(function () {
    'use strict';

    angular
        .module('capvalue.bulk.controllers')
        .controller('IpNeghboursController', IpNeghboursController);

    IpNeghboursController.$inject = ['Authentication', '$state'];

    function IpNeghboursController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();
