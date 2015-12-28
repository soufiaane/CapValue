(function () {
    'use strict';

    angular
        .module('capvalue.job.services')
        .factory('Job', Job);

    Job.$inject = ['$cookies', '$http'];


    function Job($cookies, $http) {

        return Job = {
            logg: logg
        };

        function logg(message) {
            return console.log(message);
        }
    }
})();