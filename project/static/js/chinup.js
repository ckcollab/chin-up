var chinupApp = angular.module('chinupApp', ['ngCookies']);

chinupApp
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    })
    .run(function($rootScope, $log, $http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $('input[name="csrfmiddlewaretoken"]').val();
    });

// Get parameters
var get_params = decodeURIComponent(window.location.search.slice(1))
                      .split('&')
                      .reduce(function _reduce (/*Object*/ a, /*String*/ b) {
                        b = b.split('=');
                        a[b[0]] = b[1];
                        return a;
                      }, {});

function ChinupController($scope, $http, $location) {
    $scope.metrics = {};
    $scope.save_text = "Save";
    $scope.date = get_params['date'] || '';

    $scope.save_metrics = function() {
        $scope.save_text = "Saving...";

        $scope.metric_form['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();

        $http({
            method: 'POST',
            url: '/input/?date=' + $scope.date,
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

    $scope.convert_measurement_to_hsl = function(value){
        var hue = ((value * 12) - 12);
        var sat = '50%';
        var l = '65%';

        // Skip gold color, make it gray
        if(value == 5) {
            sat = '0%';
        } else if (value > 5) {
            hue += 24;
        }

        return 'hsl(' + hue + ', ' + sat + ', ' + l + ')';
    };

    $scope.init_recording = function(record_pk, type, value) {
        if($scope.metrics[record_pk] === undefined) {
            $scope.metrics[record_pk] = {}
        }

        $scope.metrics[record_pk][type] = value;

        console.log($scope.metrics[record_pk][type]);
    };
}
