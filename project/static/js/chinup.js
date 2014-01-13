var chinupApp = angular.module('chinupApp', []);

chinupApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

function ChinupController($scope) {
    $scope.metrics = {};
}
