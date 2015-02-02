var main = angular.module('test', ['ngResource']);
        
main.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{(');
  $interpolateProvider.endSymbol(')}');
});

