(function () {
    'use strict';

    angular
        .module('capvalue.seed.services')
        .factory('Seed', Seed)
        .factory('FileUpload', FileUpload);

    Seed.$inject = ['$cookies', '$http'];
    FileUpload.$inject = ['$http'];

    function Seed($cookies, $http) {
        return Seed = {
            logg: logg
        };

        function logg(message) {
            return console.log(message);
        }
    }

    function FileUpload($http) {
        var FileUpload = {
            uploadFileToUrl: uploadFileToUrl
        };

        return FileUpload;

        function uploadFileToUrl(file, uploadUrl) {
            var fd = new FormData();
            fd.append('file', file);
            $http.post(uploadUrl, fd, {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined}
                })
                .success(function () {
                })
                .error(function () {
                });
        }
    }

})();