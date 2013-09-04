var app = angular.module('app', ['controllers']);

var controllers = angular.module('controllers', []);

controllers.controller('AppController', ['$scope', '$http', function($scope, $http) {
    // load data
    $http.get('data/resultados.csv')
        .success(function(csv) {
            $scope.games = $.csv.toObjects(csv);
            console.log($scope.games);        //TODO(gb): Remove trace!!!
        })
}])