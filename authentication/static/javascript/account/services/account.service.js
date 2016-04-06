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
            var url = '/api/v1/accounts/profiles/?page=' + page;
            if (filter.id) {url += ('&id=' + filter.id);}
            if (filter.username) {url += ('&username=' + filter.username);}
            if (filter.first_name) {url += ('&first_name=' + filter.first_name);}
            if (filter.last_name) {url += ('&last_name=' + filter.last_name);}
            if (filter.entity) {url += ('&entity=' + filter.entity);}
            if (filter.team) {url += ('&team=' + filter.team);}
            if (filter.role) {url += ('&role=' + filter.role);}
            if (filter.created_at) {url += ('&created_at=' + filter.created_at);}
            if (sorting.id && sorting.id === "desc") {url += '&ordering=-id'; return $http.get(url);}
            if (sorting.id && sorting.id === "asc") {url += '&ordering=id'; return $http.get(url);}
            if (sorting.username && sorting.username === "desc") {url += '&ordering=-username'; return $http.get(url);}
            if (sorting.username && sorting.username === "asc") {url += '&ordering=username'; return $http.get(url);}
            if (sorting.first_name && sorting.first_name === "desc") {url += '&ordering=-first_name'; return $http.get(url);}
            if (sorting.first_name && sorting.first_name === "asc") {url += '&ordering=first_name'; return $http.get(url);}
            if (sorting.last_name && sorting.last_name === "desc") {url += '&ordering=-last_name'; return $http.get(url);}
            if (sorting.last_name && sorting.last_name === "asc") {url += '&ordering=last_name'; return $http.get(url);}
            if (sorting.entity && sorting.entity === "desc") {url += '&ordering=-entity'; return $http.get(url);}
            if (sorting.entity && sorting.entity === "asc") {url += '&ordering=entity'; return $http.get(url);}
            if (sorting.team && sorting.team === "desc") {url += '&ordering=-team'; return $http.get(url);}
            if (sorting.team && sorting.team === "asc") {url += '&ordering=team'; return $http.get(url);}
            if (sorting.role && sorting.role === "desc") {url += '&ordering=-role'; return $http.get(url);}
            if (sorting.role && sorting.role === "asc") {url += '&ordering=role'; return $http.get(url);}
            if (sorting.created_at && sorting.created_at === "desc") {url += '&ordering=-created_at'; return $http.get(url);}
            if (sorting.created_at && sorting.created_at === "asc") {url += '&ordering=created_at'; return $http.get(url);}
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