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
            get: get,
            get_job: get_job,
            revoke_job: revoke_job,
            delete_Job: delete_Job
        };

        function all() {
            return $http.get('/api/v1/jobs/');
        }
        function get_job(job_id) {
            return $http.get('/api/v1/jobs/');
        }


        function get(username, page) {
            return $http.get('/api/v1/accounts/' + username + '/job/?page=' + page);
        }

        function revoke_job(celery_id) {
            return $http.post('/api/v1/jobs/revoke/', {
                celery_id: celery_id
            });
        }

        function delete_Job(job_id){
            return $http.delete('/api/v1/jobs/' + job_id + '/');
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