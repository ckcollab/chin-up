function CorrelationsController($scope, $http, $location) {
    $scope.resize_graph = function() {
        setTimeout(function() {
            $(window).resize();
        }, 1);
    };
}
