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
            return $http.get('/api/v1/seeds/' + username + '/');
        }

        function create(list_name, proxyType, emails) {
            var emails_created = [];

            for (var i = 0; i < emails["files"].length; i++) {
                emails_created.push(emails["files"][i]);
            }

            for (var l = 0; l < emails["textarea"].length; l++) {
                emails_created.push(emails["textarea"][i]);
            }

            return $http.post('/api/v1/seeds/', {
                emails: emails_created,
                list_name: list_name,
                proxyType: proxyType
            });
        }
    }
})();