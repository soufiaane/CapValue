(function () {
    'use strict';

    angular
        .module('capvalue.account.services')
        .factory('Account', Account);

    Account.$inject = ['$http'];

    function Account($http) {
        return Proxy = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            return $http.get('/api/v1/accounts/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/jobs/');
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