(function () {
    'use strict';

    angular
        .module('capvalue.proxies.controllers')
        .controller('ProxyCreateController', ProxyCreateController);

    ProxyCreateController.$inject = ['Authentication', '$state'];

    function ProxyCreateController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();




