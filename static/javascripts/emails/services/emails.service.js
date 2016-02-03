(function () {
    'use strict';

    angular
        .module('capvalue.emails.services')
        .factory('Emails', Emails);

    Emails.$inject = ['$http'];

    function Emails($http) {
        return Emails = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/emails/');
        }

        function get(username, page) {
            return $http.get('/api/v1/emails/' + username + '/');
        }

        function create(email) {
            return $http.post('/api/v1/emails/', {
                email: email['email'],
                password: email['password']
            });
        }
    }
})();