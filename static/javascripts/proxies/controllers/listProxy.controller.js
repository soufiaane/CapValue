(function () {
    'use strict';

    angular
        .module('capvalue.proxies.controllers')
        .controller('ProxyListController', ProxyListController);

    ProxyListController.$inject = ['Authentication', '$state'];

    function ProxyListController(Authentication) {
        var vm = this;
    }

})();




