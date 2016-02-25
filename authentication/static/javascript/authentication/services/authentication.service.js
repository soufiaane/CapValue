(function () {
    'use strict';

    angular
        .module('capvalue.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http', '$state'];


    function Authentication($cookies, $http) {

        return Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate
        };

        function register(password, username, fname, lname) {
            return $http.post('api/v1/accounts/', {
                first_name: fname,
                last_name: lname,
                password: password,
                username: username
            });
        }

        function login(username, password) {
            return $http.post('api/v1/auth/login/', {
                username: username,
                password: password
            }).then(loginSuccessFn, loginErrorFn);

            function loginSuccessFn(data) {
                Authentication.setAuthenticatedAccount(data.data);
                window.location = '/';
            }

            function loginErrorFn() {
                console.error('Error login in the User !');
            }
        }

        function logout() {
            return $http.post('api/v1/auth/logout/').then(logoutSuccessFn, logoutErrorFn);

            function logoutSuccessFn() {
                Authentication.unauthenticate();
                window.location = '/';
            }

            function logoutErrorFn() {
                Snackbar.error('Error login out the User !');
            }
        }

        function getAuthenticatedAccount() {
            var authAccount = $cookies.get('authenticatedAccount');
            if (!authAccount) {
                return false;
            }

            return JSON.parse(authAccount);
        }

        function isAuthenticated() {
            return !!$cookies.get('authenticatedAccount');
        }

        function setAuthenticatedAccount(account) {
            $cookies.put('authenticatedAccount', JSON.stringify(account));
        }

        function unauthenticate() {
            $cookies.remove('authenticatedAccount');
        }
    }
})();