(function ($, _) {
    'use strict';

    angular
        .module('capvalue.utils.services')
        .factory('Snackbar', Snackbar);

    /**
     * @namespace Snackbar
     */
    function Snackbar() {
        /**
         * @name Snackbar
         * @desc The factory to be returned
         */
        var Snackbar = {
            error: error,
            show: show
        };

        return Snackbar;

        ////////////////////

        /**
         * @name _snackbar
         * @desc Display a snackbar
         * @param {string} content The content of the snackbar
         * @param {Object} options Options for displaying the snackbar
         */
        function _snackbar(content, options) {
            options = {
                style: "toast", // add a custom class to your snackbar
                timeout: 1000, // time in milliseconds after the snackbar autohides, 0 is disabled
                htmlAllowed: true // allows HTML as content value
            };
            options = _.extend({timeout: 3000}, options);
            options.content = content;

            $.snackbar(options);
        }


        /**
         * @name error
         * @desc Display an error snackbar
         * @param {string} content The content of the snackbar
         * @param {Object} options Options for displaying the snackbar
         * @memberOf capvalue.utils.services.Snackbar
         */
        function error(content, options) {
            options = {
                style: "toast", // add a custom class to your snackbar
                timeout: 1000, // time in milliseconds after the snackbar autohides, 0 is disabled
                htmlAllowed: true // allows HTML as content value
            };
            _snackbar('Error: ' + content, options);
        }


        /**
         * @name show
         * @desc Display a standard snackbar
         * @param {string} content The content of the snackbar
         * @param {Object} options Options for displaying the snackbar
         * @memberOf capvalue.utils.services.Snackbar
         */
        function show(content, options) {
            options = {
                style: "toast", // add a custom class to your snackbar
                timeout: 1000, // time in milliseconds after the snackbar autohides, 0 is disabled
                htmlAllowed: true // allows HTML as content value
            };
            _snackbar(content, options);
        }
    }
})($, _);