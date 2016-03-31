(function () {
    'use strict';

    angular
        .module('capvalue.isp.services')
        .factory('ISP', ISP);

    ISP.$inject = ['$http'];

    function ISP($http) {
        return ISP = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/isps/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/isp/');
        }

        function create(email) {
            return $http.post('/api/v1/emails/', {
                email: email['email'],
                password: email['password']
            });
        }


    }
})();