function StatsController($scope, $http, $location) {
    $scope.select_graph = function(graph_name) {
        localStorage.setItem("last_graph_name", graph_name);

        $scope.graph_name = graph_name;
        setTimeout(function() {
            $(window).resize();
        }, 1);

    };

    $scope.is_graph_showing = function(graph_name) {
        return $scope.graph_name === graph_name;
    };

    // Init
    $scope.init_graphs = function() {
        var graph_name = localStorage.getItem("last_graph_name") || "month-to-month";

        $scope.select_graph(graph_name);
    };
}
