(function () {
    'use strict';

    angular
        .module('capvalue.proxy.controllers')
        .controller('ProxyListController', ProxyListController);

    ProxyListController.$inject = ['Authentication', '$state'];

    function ProxyListController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();




