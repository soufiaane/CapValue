(function () {
    'use strict';

    angular
        .module('capvalue.seed.services')
        .factory('Seed', Seed);

    Seed.$inject = ['$http'];

    function Seed($http) {
        return Seed = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/seeds/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/seeds/');
        }

        function create(list_name, proxyType) {
            return $http.post('/api/v1/seeds/', {
                list_name: list_name,
                proxyType: proxyType
            });
        }
    }
})();