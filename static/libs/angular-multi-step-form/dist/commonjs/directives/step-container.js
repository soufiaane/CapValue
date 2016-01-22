<<<<<<< HEAD
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});
exports['default'] = stepContainer;

/**
 * @ngdoc    directive
 * @name     multiStepForm:stepContainer
 *
 * @requires multiStepForm:stepContainer
 *
 * @restrict A
 * @description The container for form steps. It registers itself with the multi step container.
 *              {@link multiStepForm:multiStepContainer multiStepContainer}
 *
 * @ngInject
 */
function stepContainer() {
    return {
        restrict: 'EA',
        require: '^^multiStepContainer',
        scope: false,
        link: function postLink(scope, element, attrs, multiStepCtrl) {
            element.addClass('multi-step-body');
            multiStepCtrl.setStepContainer(element);
        }
    };
}
=======
'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});
exports['default'] = stepContainer;

/**
 * @ngdoc    directive
 * @name     multiStepForm:stepContainer
 *
 * @requires multiStepForm:stepContainer
 *
 * @restrict A
 * @description The container for form steps. It registers itself with the multi step container.
 *              {@link multiStepForm:multiStepContainer multiStepContainer}
 *
 * @ngInject
 */
function stepContainer() {
    return {
        restrict: 'EA',
        require: '^^multiStepContainer',
        scope: false,
        link: function postLink(scope, element, attrs, multiStepCtrl) {
            element.addClass('multi-step-body');
            multiStepCtrl.setStepContainer(element);
        }
    };
}
>>>>>>> 942286391f24f61d690faaf4c33948109167ed24
module.exports = exports['default'];