(function () {
    'use strict';

    angular
        .module('capvalue.proxies.controllers')
        .controller('ProxyCreateController', ProxyCreateController);

    ProxyCreateController.$inject = ['Authentication', '$state', 'Snackbar', 'Proxy'];

    function ProxyCreateController(Authentication, $state, Snackbar, Proxy) {
        var vm = this;
        vm.submitProxy = submitProxy;
        vm.proxyListInputBind = proxyListInputBind;
        vm.proxy = {ip: {textarea: [], files: [], all: []}, proxy_type: ""};
        activate();

        function proxyListInputBind(type) {
            if (type == "file") {

            }
            else if (type == 'textarea') {
                vm.proxy.ip["textarea"] = [];
                var data = Papa.parse(vm.proxy.textarea_Input).data;
                for (var l = 0; l < data.length; l++) {
                    if (data[l].length >= 2) {
                        vm.proxy.ip['textarea'].push({
                            'ip': data[l][0],
                            'port': data[l][1],
                            'login': (data[l][2]) ? data[l][2] : "",
                            'pass': (data[l][3]) ? data[l][3] : ""
                        });
                    }
                }
            }
        }

        function submitProxy() {
            if (vm.proxy.ip['textarea']) {
                for (var i = 0; i < vm.proxy.ip['textarea'].length; i++) {
                    vm.proxy.ip['all'].push(
                        vm.proxy.ip['textarea'][i]
                    );
                }
            }
            if (vm.proxy.ip['file']) {
                for (var l = 0; l < vm.proxy.ip['file'].length; l++) {
                    vm.proxy.ip['all'].push(
                        vm.proxy.ip['file'][l]
                    );
                }
            }
            Proxy.create(vm.proxy)
                .then(createProxySuccessFn, createProxyErrorFn);

            function createProxySuccessFn() {
                Snackbar.show('Proxy List Created Successfully');
                $state.go($state.current, {}, {reload: true});
            }

            function createProxyErrorFn() {
                Snackbar.error('Error when attempting to Create Proxy');
            }
        }

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $state.go('Login');
            }
            vm.proxy.proxy_type = "Proxy"
        }
    }

})();




