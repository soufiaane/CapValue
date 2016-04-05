(function () {
    'use strict';

    angular
        .module('capvalue.account.services')
        .factory('Account', Account);

    Account.$inject = ['$http'];

    function Account($http) {
        return Account = {
            all: all,
            get: get
        };


        function all(page, filter, sorting, count) {
            var url = '/api/v1/accounts/?page=' + page ;
            if (filter.name){url += ('&name=' + filter.name);}
            if (filter.id){url += ('&id=' + filter.id);}
            if(sorting.name && sorting.name === "desc"){url += '&ordering=-name'; return $http.get(url);}
            if(sorting.name && sorting.name === "asc"){url += '&ordering=name'; return $http.get(url);}
            if(sorting.id && sorting.id === "desc"){url += '&ordering=-id'; return $http.get(url);}
            if(sorting.id && sorting.id === "asc"){url += '&ordering=id'; return $http.get(url);}
            return $http.get(url);
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