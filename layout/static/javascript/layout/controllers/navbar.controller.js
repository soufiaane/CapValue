(function () {
    'use strict';

    angular
        .module('capvalue.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['Authentication', 'ISP'];

    function NavbarController(Authentication, ISP) {
        var vm = this;
        vm.logout = logout;
        vm.showIspLogo = false;

        function logout() {
            Authentication.logout();
        }

        function activate() {
            vm.user = Authentication.getAuthenticatedAccount();
            ISP.get(vm.user.username).then(getUserIspSuccess, getUserIspError);

            function getUserIspSuccess(results) {
                vm.isp = results.data[0];
                vm.showIspLogo = true;
            }

            function getUserIspError(e) {
                console.log(e);
            }
        }

        activate();
    }
})();