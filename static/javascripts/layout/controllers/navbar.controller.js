(function () {
    'use strict';

    angular
        .module('capvalue.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['Authentication'];

    function NavbarController(Authentication) {
        var vm = this;

        vm.logout = logout;

        function logout() {
            Authentication.logout();
        }
    }
})();