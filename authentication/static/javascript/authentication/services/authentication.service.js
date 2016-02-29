(function () {
    'use strict';

    angular
        .module('capvalue.authentication.services')
        .factory('Notifications', Notifications)
        .factory('Authentication', Authentication);

    Notifications.$inject = ['socketFactory'];
    Authentication.$inject = ['$cookies', '$http', 'Notifications'];

    function Notifications(socketFactory) {
        var myIoSocket = io.connect('http://cvc.ma:3000');

        return socketFactory({
            ioSocket: myIoSocket
        });

    }

    function Authentication($cookies, $http, Notifications) {

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
                Notifications.emit('message', 'Taboun 3achwa2i\n' + data.data);
            }

            function loginErrorFn() {
                console.error('loginErrorFn');
            }
        }

        function logout() {
            return $http.post('api/v1/auth/logout/').then(logoutSuccessFn, logoutErrorFn);

            function logoutSuccessFn() {
                Authentication.unauthenticate();
                window.location = '/';
            }

            function logoutErrorFn() {
                Snackbar.error('logoutErrorFn');
            }
        }

        function getAuthenticatedAccount() {
            var authAccount = $cookies.get('authenticatedAccount');

            if (!authAccount) {
                return false;
            } else {
                var result = JSON.parse(authAccount);
                result.role[0] = toTitleCase(result.role[0]);
                return result;
            }
        }

        function toTitleCase(str) {
            return str.replace(/\w\S*/g, function (txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
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