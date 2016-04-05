(function () {
    'use strict';

    angular
        .module('capvalue.bulk.controllers')
        .controller('SpfCheckController', SpfCheckController);

    SpfCheckController.$inject = ['Authentication', '$state'];

    function SpfCheckController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();
