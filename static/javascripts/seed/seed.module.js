(function () {
    'use strict';

    angular
        .module('capvalue.seed', [
            'capvalue.seed.controllers',
            'capvalue.seed.services',
            'capvalue.seed.directives',
            'ngAnimate',
            'multiStepForm'
        ]);

    angular
        .module('capvalue.seed.controllers', ['multiStepForm']);

    angular
        .module('capvalue.seed.services', ['multiStepForm']);

    angular
        .module('capvalue.seed.directives', ['multiStepForm']);
})();