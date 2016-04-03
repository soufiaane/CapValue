(function () {
    'use strict';

    angular
        .module('capvalue.seed.services')
        .factory('Seed', Seed);

    Seed.$inject = ['$http'];

    function Seed($http) {
        return Seed = {
            all: all,
            create: create,
            get: get,
            dell: dell,
            get_seed: get_seed,
            get_seed_emails: get_seed_emails
        };

        function all() {
            return $http.get('/api/v1/seeds/');
        }

        function get(username, page, filter, sorting, count) {
            var url = '/api/v1/accounts/' + username + '/seed/?page=' + page ;
            if (filter.name){url += ('&name=' + filter.name);}
            if (filter.id){url += ('&id=' + filter.id);}
            if(sorting.name && sorting.name === "desc"){url += '&ordering=-name'; return $http.get(url);}
            if(sorting.name && sorting.name === "asc"){url += '&ordering=name'; return $http.get(url);}
            if(sorting.id && sorting.id === "desc"){url += '&ordering=-id'; return $http.get(url);}
            if(sorting.id && sorting.id === "asc"){url += '&ordering=id'; return $http.get(url);}
            return $http.get(url);
        }

        function get_seed(seed_id) {
            return $http.get('/api/v1/seeds/' + seed_id + '/');
        }

        function get_seed_emails(seed_id) {
            return $http.get('/api/v1/emails/seed/' + seed_id + '/');
        }

        function create(list_name, emails) {
            var mails = [];

            for (var i = 0; i < emails["textarea"].length; i++) {
                mails.push(emails["textarea"][i]);
            }

            return $http.post('/api/v1/seeds/', {
                emails: mails,
                list_name: list_name,
                proxyType: 'manual'
            });
        }

        function dell(seed_id){
            return $http.delete('/api/v1/seeds/' + seed_id + '/');
        }
    }
})();