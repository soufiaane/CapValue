(function () {
    'use strict';

    angular
        .module('capvalue.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['Authentication', 'ISP', '$rootScope', '$scope'];

    function NavbarController(Authentication, ISP, $rootScope, $scope) {
        var vm = this;
        activate();
        vm.logout = logout;

        function logout() {
            Authentication.logout();
        }

        function activate() {
            $rootScope.isp_name = {
                show: false,
                name: '',
                logo: ''
            };
            if (Authentication.isAuthenticated()) {
                vm.user = Authentication.getAuthenticatedAccount();
                if (vm.user.role != 'Manager') {
                    ISP.get_isp_team(vm.user.teams[0]).then(function (results) {
                        vm.isp = results.data[0];
                        $rootScope.isp_name = {
                            show: true,
                            name: vm.isp.isp_name,
                            logo: vm.isp.logo
                        };
                        $scope.isp_name = $rootScope.isp_name;
                    });
                }
            }
        }
    }
})();