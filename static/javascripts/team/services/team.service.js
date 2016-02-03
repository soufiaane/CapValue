(function () {
    'use strict';

    angular
        .module('capvalue.team.services')
        .factory('Team', Team);

    Team.$inject = ['$http'];

    function Team($http) {
        return Team = {
            all: all,
            create: create,
            get: get,
            get_team_isp: get_team_isp
        };

        function get_team_isp(isp_id) {
            return $http.get('/api/v1/teams/isp/' + isp_id + '/');
        }

        function all() {
            return $http.get('/api/v1/isps/');
        }

        function get(username) {
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