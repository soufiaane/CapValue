(function () {
    'use strict';

    angular
        .module('capvalue.posts.directives')
        .directive('post', post);

    function post() {
        var directive = {
            restrict: 'E',
            scope: {
                post: '='
            },
            templateUrl: '/static/templates/posts/post.html'
        };

        return directive;
    }
})();