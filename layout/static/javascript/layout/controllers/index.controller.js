(function () {
    'use strict';
    angular
        .module('capvalue.layout.controllers')
        .controller('IndexController', IndexController);
    IndexController.$inject = ['Authentication', '$state'];

    function IndexController(Authentication, $state) {
        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }

        activate();
    }
})();