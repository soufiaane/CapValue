(function () {
    'use strict';

    angular
        .module('capvalue.seed.services')
        .factory('Seed', Seed);

    Seed.$inject = ['$cookies', '$http'];


    function Seed($cookies, $http) {

        return Seed = {
            logg: logg
        };

        function logg(message) {
            return console.log(message);
        }
    }
})();