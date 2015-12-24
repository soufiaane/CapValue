(function () {
    'use strict';

    angular
        .module('capvalue.posts', [
            'capvalue.posts.controllers',
            'capvalue.posts.directives',
            'capvalue.posts.services'
        ]);

    angular
        .module('capvalue.posts.controllers', []);

    angular
        .module('capvalue.posts.directives', ['ngDialog']);

    angular
        .module('capvalue.posts.services', []);
})();