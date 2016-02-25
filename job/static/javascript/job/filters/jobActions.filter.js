(function () {
    'use strict';
    angular
        .module('capvalue.job.filters', [])
        .filter('split', split);
    split.$inject = ['$sce'];

    function split($sce) {
        return split = function (input) {
            var splitted = input.split(',');
            var results = "";
            for(var i =0; i<splitted.length;i++){
                results += "<span class=\"badge label label-info\" >" + splitted[i] + '</span>&nbsp;'
            }
            return $sce.trustAsHtml(results);
        };
    }
})();