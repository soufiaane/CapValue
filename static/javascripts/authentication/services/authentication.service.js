(function () {
    'use strict';

    angular
        .module('capvalue.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http', '$state', 'Snackbar'];


    function Authentication($cookies, $http, Snackbar) {

        return Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate
        };

        function register(password, username) {
            return $http.post('/api/v1/accounts/', {
                password: password,
                username: username
            }).then(registerSuccessFn, registerErrorFn);
            function registerSuccessFn() {
                Snackbar.show('User Created Successfully !');
                Authentication.login(username, password);
            }

            function registerErrorFn() {
                Snackbar.error('Error Creating a new User !');
            }
        }

        function login(username, password) {
            return $http.post('/api/v1/auth/login/', {
                username: username,
                password: password
            }).then(loginSuccessFn, loginErrorFn);

            function loginSuccessFn(data) {
                Authentication.setAuthenticatedAccount(data.data);
                window.location = '/';
            }

            function loginErrorFn() {
                Snackbar.error('Error login in the User !');
            }
        }

        function logout() {
            return $http.post('/api/v1/auth/logout/').then(logoutSuccessFn, logoutErrorFn);

            function logoutSuccessFn() {
                Authentication.unauthenticate();
                //$state.go('Home', {}, {reload: true});
                //TODO-CVC use $state
                window.location = '/';
            }

            function logoutErrorFn() {
                Snackbar.error('Error login out the User !');
            }
        }

        function getAuthenticatedAccount() {
            var authAccount = $cookies.get('authenticatedAccount');
            if (!authAccount) {
                return;
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