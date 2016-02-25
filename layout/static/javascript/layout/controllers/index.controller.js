(function () {
    'use strict';
    angular
        .module('capvalue.layout.controllers')
        .controller('IndexController', IndexController);
    IndexController.$inject = ['Authentication', '$state'];
    function IndexController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
        vm.isAuthenticated = Authentication.isAuthenticated();
    }
})();