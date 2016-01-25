(function () {
    'use strict';

    angular
        .module('capvalue.job.services')
        .factory('Job', Job);

    Job.$inject = ['$http'];

    function Job($http) {
        return Job = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/jobs/');
        }

        function get(username, page) {
            if (!page) {
                return $http.get('/api/v1/jobs/' + username + '/');
            }
            return $http.get('/api/v1/jobs/' + username + '/?page=' + page);
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