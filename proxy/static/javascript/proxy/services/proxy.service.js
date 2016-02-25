(function () {
    'use strict';

    angular
        .module('capvalue.proxy.services')
        .factory('Proxy', Proxy);

    Proxy.$inject = ['$http'];

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

        function create(proxy) {
            return $http.post('/api/v1/proxy/', {
                proxy_name: proxy["name"],
                proxy_type: proxy["proxy_type"],
                ips: proxy["ip"]["all"]
            });
        }
    }
})();