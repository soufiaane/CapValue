(function () {
    'use strict';

    angular
        .module('capvalue.proxies.controllers')
        .controller('ProxyCreateController', ProxyCreateController);

    ProxyCreateController.$inject = ['Authentication', '$state'];

    function ProxyCreateController(Authentication) {
        var vm = this;
    }

})();




