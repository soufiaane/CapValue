(function () {
    'use strict';

    angular
        .module('capvalue.account.services')
        .factory('Account', Account);

    Account.$inject = ['$http', 'ISP'];

    function Account($http, ISP) {
        return Account = {
            all: all,
            create: create,
            get: get
        };

        function all() {
            $http.get('/api/v1/accounts/').then(SuccessAccountListFn, ErrorAccountListFn);
            function SuccessAccountListFn(results) {
                var accounts = [];
                for (var i = 0; i < results.data.count; i++) {
                    var account = results.data.results[i];
                    var teams = [];
                    for (var k = 0; k < account.teams.length; k++) {
                        teams.push();
                    }
                    account.isp = '';

                }
                console.log(results);
            }

            function ErrorAccountListFn() {

            }
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