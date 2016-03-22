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
            get: get,
            dell: dell,
            get_seed: get_seed,
            get_seed_emails: get_seed_emails
        };

        function all() {
            return $http.get('/api/v1/seeds/');
        }

        function get(username, page) {
            if (page > 1) {
                return $http.get('/api/v1/accounts/' + username + '/seed/?page=' + page);
            }
            else {
                return $http.get('/api/v1/accounts/' + username + '/seed/');
            }
        }

        function get_seed(seed_id) {
            return $http.get('/api/v1/seeds/');
        }

        function get_seed_emails(seed_id) {
            return $http.get('/api/v1/emails/seed/' + seed_id + '/');
        }

        function create(list_name, proxyType, emails) {
            var mails = [];

            for (var i = 0; i < emails["files"].length; i++) {
                mails.push(emails["files"][i]);
            }

            for (var l = 0; l < emails["textarea"].length; l++) {
                mails.push(emails["textarea"][l]);
            }

            return $http.post('/api/v1/seeds/', {
                emails: mails,
                list_name: list_name,
                proxyType: proxyType
            });
        }

        function dell(seed_id){
            return $http.delete('/api/v1/seeds/' + seed_id + '/');
        }
    }
})();