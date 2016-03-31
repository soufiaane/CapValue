(function () {
    'use strict';

    angular
        .module('capvalue.account.services')
        .factory('Account', Account);

    Account.$inject = ['$http', 'Notifications'];

    function Account($http, Notifications) {
        return Account = {
            all: all,
            get: get
        };


        function all() {
            return $http.get('/api/v1/accounts/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/');
        }

        function SuccessAccountListFn(results) {
            for (var i = 0; i < results.data.count; i++) {
                var account = results.data.results[i];
                var teams = [];
                for (var k = 0; k < account.teams.length; k++) {
                    teams.push();
                }
                account.isp = '';
            }
        }
    }
})();