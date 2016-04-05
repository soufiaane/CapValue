(function () {
    'use strict';

    angular
        .module('capvalue.bulk.controllers')
        .controller('FindSubjectController', FindSubjectController);

    FindSubjectController.$inject = ['Authentication', '$state'];

    function FindSubjectController(Authentication, $state) {
        var vm = this;
        activate();

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
        }
    }

})();
