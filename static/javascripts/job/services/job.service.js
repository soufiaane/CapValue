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

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/jobs/');
        }

        function create(list_name, proxyType) {
            return $http.post('/api/v1/jobs/', {
                list_name: list_name,
                proxyType: proxyType
            }).then(createSuccessFn, createErrorFn);

            function createSuccessFn() {
                console.log('SUCCESSSSSSSSSSSSSS');
            }

            function createErrorFn() {
                console.error('Epic failure! (seed.service.create.createErrorFn)');
            }
        }
    }
})();