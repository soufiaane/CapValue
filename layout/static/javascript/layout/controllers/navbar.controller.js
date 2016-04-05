(function () {
    'use strict';

    angular
        .module('capvalue.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['Authentication', 'Team'];

    function NavbarController(Authentication, Team) {
        var vm = this;

        vm.logout = logout;
        vm.showIspLogo = false;

        function logout() {
            Authentication.logout();
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                vm.user = Authentication.getAuthenticatedAccount();
                Team.get(vm.user.username).then(getUserTeamSuccess, getUserTeamError);
            }
            function getUserTeamSuccess(results) {
                vm.isp = results.data[0];
                vm.showIspLogo = true;
            }

            function getUserTeamError(e) {
                console.log(e);
            }
        }

        activate();
    }
})();