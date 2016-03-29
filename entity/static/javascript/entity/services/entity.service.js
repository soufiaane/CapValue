(function () {
    'use strict';

    angular
        .module('capvalue.entity.services')
        .factory('Entity', Entity);

    Entity.$inject = ['$http'];

    function Entity($http) {
        return Entity = {
            all: all,
            create: create,
            get: get,
            get_teams: get_teams
        };

        function get_teams(entity_id) {
            return $http.get('/api/v1/entity/' + entity_id + '/teams/');
        }

        function all() {
            return $http.get('/api/v1/entity/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/entity/');
        }


        function create(email) {
            return $http.post('/api/v1/emails/', {
                email: email['email'],
                password: email['password']
            });
        }
    }
})();