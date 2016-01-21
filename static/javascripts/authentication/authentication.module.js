(function () {
    'use strict';

    angular
        .module('capvalue.authentication', [
            'capvalue.authentication.controllers',
            'capvalue.authentication.services'
        ]);

    angular
        .module('capvalue.authentication.controllers', []);

    angular
        .module('capvalue.authentication.services', ['ngCookies']);
})();