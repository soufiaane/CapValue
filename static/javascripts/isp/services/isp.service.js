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
            get: get,
            get_isp_team: get_isp_team
        };

        function all() {
            return $http.get('/api/v1/isps/');
        }

        function get(username, page) {
            return $http.get('/api/v1/emails/' + username + '/?page=' + page);
        }

        function create(email) {
            return $http.post('/api/v1/emails/', {
                email: email['email'],
                password: email['password']
            });
        }

        function get_isp_team(team_id) {
            return $http.get('/api/v1/isps/team/' + team_id + '/');
        }
    }
})();