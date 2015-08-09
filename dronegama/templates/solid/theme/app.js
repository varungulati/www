angular.module('ui.router.util', ['ng', 'ngRoute']);
angular.module('ui.router.router', ['ui.router.util']);
angular.module('ui.router.state', ['ui.router.router', 'ui.router.util']);
angular.module('ui.router', ['ui.router.state']);
angular.module('ui.router.compat', ['ui.router']);

var app = angular.module('app', ['ui.router.compat'])
  .config(function($routeProvider) {
      $routeProvider
        .when(
            '/home',
            {
              templateUrl: '/partials/home.html',
            })
        .when(
            '/aboutus',
            {
              templateUrl: '/partials/about_us.html'
            }
          )
        .when(
            '/contactus',
            {
              templateUrl: '/partials/contact_us.html'
            }
          )
        .otherwise(
            {
              redirectTo: '/home'
            }
          )
  });