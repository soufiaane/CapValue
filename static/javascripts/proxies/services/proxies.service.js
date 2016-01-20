(function () {
    'use strict';

    angular
        .module('capvalue.proxies.services')
        .factory('Proxy', Proxy);

    Job.$inject = ['$http'];

    function Proxy($http) {
        return Proxy = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/jobs/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/jobs/');
        }

        function create(keyword, seed_list, actions) {
            return $http.post('/api/v1/jobs/', {
                keywords: keyword,
                seed_list: seed_list,
                actions: actions
            });
        }
    }
})();