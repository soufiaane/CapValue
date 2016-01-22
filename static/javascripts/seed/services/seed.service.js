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

        function get(username, page) {
            if (!page) {
                return $http.get('/api/v1/seeds/' + username + '/');
            }
            return $http.get('/api/v1/seeds/' + username + '/?page=' + page);
        }

        function create(list_name, proxyType) {
            return $http.post('/api/v1/seeds/', {
                list_name: list_name,
                proxyType: proxyType
            });
        }
    }
})();