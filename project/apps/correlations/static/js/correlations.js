function CorrelationsController($scope, $http, $location) {
    $scope.resize_graph = function() {
        console.log('window resized');
        setTimeout(function() {
            $(window).resize();
        }, 1);
    };
}
