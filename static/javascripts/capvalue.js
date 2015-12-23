(function () {
    'use strict';

    angular
        .module('capvalue', [
            'capvalue.config',
            'capvalue.routes',
            'capvalue.authentication',
            'capvalue.layout',
            //'capvalue.posts',
            //'capvalue.utils',
        ]).run(run);

    run.$inject = ['$http'];

    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }

    angular
        .module('capvalue.routes', ['ngRoute']);
    angular
        .module('capvalue.config', []);
})();
