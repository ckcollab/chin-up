var chinupApp = angular.module('chinupApp', ['ngCookies']);

chinupApp
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    })
    .run(function($rootScope, $log, $http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $('input[name="csrfmiddlewaretoken"]').val();
    });

function ChinupController($scope, $http) {
    $scope.metrics = {};
    $scope.save_text = "Save";

    $scope.save_metrics = function() {
        $scope.save_text = "Saving...";

        $scope.metric_form['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();

        $http({
            method: 'POST',
            url: '/input/',
            data: $scope.metrics,
            headers: {'X-CSRFToken': $scope.metric_form['csrfmiddlewaretoken'], 'Content-Type': "application/x-www-form-urlencoded"}
            })
            .success(function(data){
                $scope.save_text = "Saved!";
            })
            .error(function(data){
                $scope.save_text = "Error";
            });
    };
}
