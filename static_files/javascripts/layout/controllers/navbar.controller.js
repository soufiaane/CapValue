(function () {
    'use strict';

    angular
        .module('capvalue.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['Authentication', '$state'];

    function NavbarController(Authentication, $state) {
        var vm = this;
        vm.user = Authentication.getAuthenticatedAccount();
        vm.logout = logout;

        function logout() {
            Authentication.logout();
        }
    }
})();